import json
from datetime import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import BadRequest, PermissionDenied
from django.core.serializers import serialize
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from zahteve.forms import (
    DemandAnswerForm,
    MonitoringReportForm,
    RegisterForm,
    RequestRestorePasswordForm,
    RestorePasswordForm,
    VoterQuestionForm,
)
from zahteve.math import calculate_most_controversial_demands
from zahteve.models import (
    Demand,
    DemandAnswer,
    DemandState,
    Election,
    EmailVerification,
    MonitoringReport,
    Municipality,
    Newsletter,
    Party,
    ResetPassword,
    WorkGroup,
)
from zahteve.serializers import MunicipalitySerializer, PartySerializer


def amandma(request):
    return redirect(
        "https://djnd.s3.fr-par.scw.cloud/djnd/glas-ljudstva/pdf/GL-amandma-ZZVZZ-junij-2023.pdf"
    )


# Create your views here.
def after_registration(request):
    return render(request, "registration/thank_you.html")


def omnia(request):
    return redirect("https://vodici.djnd.si/zemljevid/omnia/predsedniske/1/")


def landing(request, election_slug=None):
    end_date = datetime.strptime("2026-05-15", "%Y-%m-%d").date()
    start_date = datetime.now().date()
    delta = end_date - start_date
    question_form_thankyou = False
    demands_fulfilled = 0

    # if election_slug is None:
    #     election_slug = "predsedniske-2022"

    if election_slug:

        election = Election.objects.get(slug=election_slug)

        # TODO: treba je urediti prikaz zahtev, da bodo na strani tudi tiste, ki ne pašejo pod noben work group
        work_groups = WorkGroup.objects.filter(election=election).order_by("?")

        parties = Party.objects.filter(election=election, finished_quiz=True).order_by(
            "?"
        )

        # TODO: če se bo to uporabljajo tudi za predsedniške in lokalne volitve,
        # je treba dodat election še v ta model (VoterQuestion)
        if request.method == "POST":
            voter_question_form = VoterQuestionForm(request.POST)
            if voter_question_form.is_valid():
                question_form_thankyou = True
                voter_question_form.save()
                voter_question_form = VoterQuestionForm()
                messages.success(request, "Hvala za oddano vprašanje!")
                return redirect("/")
            else:
                messages.error(request, "Prišlo je do napake.")
        else:
            voter_question_form = VoterQuestionForm()

    else:
        work_groups = []
        parties = []
        voter_question_form = VoterQuestionForm()
        question_form_thankyou = True
        election_slug = "zdravstvo-2"

        election = Election.objects.first()
        demands = Demand.objects.filter(election=election)
        # get the latest updated report for each demand
        reports = []
        for d in demands:
            related_reports = MonitoringReport.objects.filter(demand=d)
            if related_reports:
                latest_related_report = related_reports.latest("created_at")
                reports.append(latest_related_report.id)

        # all relevant monitoring objects
        mrs = MonitoringReport.objects.filter(id__in=reports)

        # all possible demand states
        all_demand_states = DemandState.objects.all().order_by("order")
        # get number of filtered promises for each status
        reports_by_states = {}
        for report in mrs:
            if reports_by_states.get(report.state.name):
                reports_by_states[report.state.name].append(report)
            else:
                reports_by_states[report.state.name] = [report]

        try:
            demands_fulfilled = len(reports_by_states["IZPOLNJENA"])
        except KeyError as e:
            print(e)

    return render(
        request,
        "zahteve/landing.html",
        context={
            "work_groups": work_groups,
            "parties": parties,
            "voter_question_form": voter_question_form,
            "question_form_thankyou": question_form_thankyou,
            "election_slug": election_slug,
            "weeks_remaining": int(delta.days / 7),
            "promises_remaining": 122 - demands_fulfilled,
        },
    )


def delovna_skupina(request, delovna_skupina_id, election_slug=None):
    try:
        delovna_skupina = WorkGroup.objects.get(id=delovna_skupina_id)
    except WorkGroup.DoesNotExist:
        return HttpResponseNotFound()

    demands = Demand.objects.filter(workgroup=delovna_skupina).order_by("?")

    og_title = delovna_skupina.og_title
    og_description = delovna_skupina.og_description

    return render(
        request,
        "zahteve/delovna_skupina.html",
        context={
            "demands": demands,
            "delovna_skupina": delovna_skupina,
            "og_title": og_title,
            "og_description": og_description,
        },
    )


def demand(request, demand_id, election_slug=None):
    # form = RegisterForm()
    try:
        demand = Demand.objects.get(id=demand_id)
    except Demand.DoesNotExist:
        return HttpResponseNotFound()

    return render(
        request,
        "zahteve/zahteva.html",
        context={
            "demand": demand,
            # 'form': form
        },
    )


def demands_party(request, party_id, election_slug=None):
    # form = RegisterForm()
    try:
        party = Party.objects.get(id=party_id)
    except Party.DoesNotExist:
        return HttpResponseNotFound()

    if party.municipality:
        work_groups = [
            {
                "id": wg.id,
                "name": wg.name,
                "demands": Demand.objects.filter(
                    election=party.election, municipality=party.municipality
                ),
            }
            for wg in WorkGroup.objects.filter(election=party.election).order_by("?")
        ]
    else:
        work_groups = WorkGroup.objects.filter(election=party.election).order_by("?")

    return render(
        request,
        "zahteve/stranka.html",
        context={
            "party": party,
            "work_groups": work_groups,
            # 'form': form
        },
    )


def faq(request):
    return render(request, "zahteve/pogosta_vprasanja.html")


def monitoring(request, election_slug=None):

    if election_slug is None:
        election = Election.objects.first()
    else:
        election = Election.objects.get(slug=election_slug)

    # demands for this election
    demands = Demand.objects.filter(election=election)
    # get the latest updated report for each demand
    reports = []
    for d in demands:
        related_reports = MonitoringReport.objects.filter(demand=d, published=True)
        if related_reports:
            latest_related_report = related_reports.latest("created_at")
            reports.append(latest_related_report.id)

    # all relevant monitoring objects
    mrs = MonitoringReport.objects.filter(id__in=reports)

    # all possible demand states
    all_demand_states = DemandState.objects.all().order_by("order")
    # get number of filtered promises for each status
    reports_by_states = {}
    for report in mrs:
        if reports_by_states.get(report.state.name):
            reports_by_states[report.state.name].append(report)
        else:
            reports_by_states[report.state.name] = [report]

    filtersForm = MonitoringReportForm(request.GET, election_id=election.id)

    if filtersForm.is_valid():
        data = filtersForm.cleaned_data

        state = data["state"]
        if state:
            mrs = mrs.filter(state=state)

        is_priority_demand = data["is_priority_demand"]
        if is_priority_demand:
            mrs = mrs.filter(demand__priority_demand=is_priority_demand)

        present_in_coalition_treaty = data["present_in_coalition_treaty"]
        if present_in_coalition_treaty:
            mrs = mrs.filter(present_in_coalition_treaty=present_in_coalition_treaty)

        cooperative = data["cooperative"]
        if cooperative:
            mrs = mrs.filter(cooperative=cooperative)

        responsible_state_bodies = data["responsible_state_bodies"]
        if responsible_state_bodies:
            mrs = mrs.filter(responsible_state_bodies__in=responsible_state_bodies)

        working_body = data["working_body"]
        if working_body:
            mrs = mrs.filter(demand__workgroup=working_body)

        sort_by = data["sort_by"]
        sort_dir = data["sort_dir"]
        if not sort_by:
            sort_by = "workgroup"
        if sort_by == "state":
            if sort_dir == "desc":
                mrs = mrs.order_by("-state__order")
            else:
                mrs = mrs.order_by("state__order")
        if sort_by == "workgroup":
            if sort_dir == "desc":
                mrs = mrs.order_by(
                    "-demand__workgroup__order", "-demand__workgroup__name"
                )
            else:
                mrs = mrs.order_by(
                    "demand__workgroup__order", "demand__workgroup__name"
                )

    else:
        print("Form is not valid")
        print(filtersForm.errors)
        filtersForm = MonitoringReportForm(election_id=election.id)

    # serialized_data = serialize("json", mrs)
    # serialized_data = json.loads(serialized_data)

    return render(
        request,
        "monitoring/index.html",
        context={
            "mrs": mrs,
            "demand_states": all_demand_states,
            "reports_by_states": reports_by_states,
            "form": filtersForm,
            "election_slug": election.slug,
            "options": {
                "yes": "DA",
                "no": "NE",
                "partially": "DELNO",
            },
        },
    )


def monitoring_report(request, monitoring_report_id):
    monitoringReport = get_object_or_404(MonitoringReport, id=monitoring_report_id)
    return render(
        request,
        "monitoring/zaveza.html",
        context={"monitoringReport": monitoringReport},
    )


@login_required
def party(request, election_slug=None):
    # Vstopna stran do vprašalnika za stranke.
    # Če uporabnik ni vpisan, ga preusmeri na login.
    # Če je vpisan, pa ni party, onemogoči dostop.
    # Če stranka še ni zaključila vprašalnika, jo preusmeri na navodila.
    # Če je stranka že zaključila vprašalnik, jo preusmeri na povzetek.

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if election_slug is None:
        election = Election.objects.first()
    else:
        election = Election.objects.get(slug=election_slug)

    if party.finished_quiz:
        return redirect(f"/{election.slug}/kandidati_ke/povzetek")
    else:
        return redirect(f"/{election.slug}/kandidati_ke/navodila")


class PartyDemand(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, category_id, election_slug=None):
        # if user is not a party, restrict access
        try:
            party = Party.objects.get(user=request.user)
        except:
            raise PermissionDenied
        # ---------------------------------------

        if election_slug is None:
            election = Election.objects.first()
        else:
            election = Election.objects.get(slug=election_slug)

        if party.finished_quiz:
            return redirect(f"/{election.slug}/kandidati_ke/povzetek")

        # for sidebar menu
        categories = WorkGroup.objects.filter(election=election).order_by("id")
        for cat in categories:
            demands = Demand.objects.filter(workgroup=cat)
            if party.municipality:
                demands = demands.filter(municipality=party.municipality)
            cat.check = len(
                DemandAnswer.objects.filter(
                    party=party, agree_with_demand__isnull=False, demand__workgroup=cat
                )
            ) == len(demands)

        # TODO: treba prilagodit za non-existend work groupe
        category = WorkGroup.objects.get(pk=category_id)
        demands = Demand.objects.filter(workgroup=category).order_by("id")
        if party.municipality:
            demands = demands.filter(municipality=party.municipality)

        DemandAnswersFormSet = forms.formset_factory(
            DemandAnswerForm, extra=len(demands)
        )
        demands_formset = DemandAnswersFormSet()

        f = []

        for demand in demands:
            da_form = {
                "demand": demand.pk,
                "party": party.pk,
                "agree_with_demand": None,
                "comment": "",
                "title": demand.title,
                "description": demand.description,
                "priority_demand": demand.priority_demand,
            }

            try:
                demand_answer = DemandAnswer.objects.get(
                    demand=demand.pk, party=party.pk
                )
                da_form["agree_with_demand"] = demand_answer.agree_with_demand
                da_form["comment"] = demand_answer.comment

            except:
                pass

            finally:
                f.append(da_form)

        return render(
            request,
            "stranke/stranke.html",
            context={
                "categories": categories,
                "category_id": category_id,
                "forms": f,
                "formset": demands_formset,
                "election_slug": election_slug,
            },
        )

    def post(self, request, category_id, election_slug=None):

        # if user is not a party, restrict access
        try:
            party = Party.objects.get(user=request.user)
        except:
            raise PermissionDenied
        # ---------------------------------------

        if election_slug is None:
            election = Election.objects.first()
        else:
            election = Election.objects.get(slug=election_slug)

        if party.finished_quiz:
            raise BadRequest

        DemandAnswersFormSet = forms.formset_factory(DemandAnswerForm)
        formset = DemandAnswersFormSet(request.POST or None)

        for form in formset:
            if form.is_valid():
                form.save()
            else:
                da = DemandAnswer.objects.get(
                    demand=form["demand"].value(), party=party.pk
                )
                da.agree_with_demand = form["agree_with_demand"].value()
                if da.agree_with_demand == "True":
                    da.comment = ""
                else:
                    comment_value = form["comment"].value()
                    if len(comment_value) > 1000:
                        comment_value = comment_value[0:1000]
                    da.comment = comment_value
                da.save()

        next = WorkGroup.objects.filter(id__gt=category_id).order_by("id").first()
        if next:
            return redirect(f"/{election.slug}/kandidati_ke/{next.id}")
        else:
            return redirect(f"/{election.slug}/kandidati_ke/oddaja")


@login_required
def party_instructions(request, election_slug=None):

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if election_slug is None:
        election = Election.objects.first()
    else:
        election = Election.objects.get(slug=election_slug)

    if party.finished_quiz:
        return redirect(f"/{election_slug}/kandidati_ke/povzetek")

    categories = WorkGroup.objects.filter(election=election).order_by("id")

    for cat in categories:
        demands = Demand.objects.filter(workgroup=cat, election=election)
        if party.municipality:
            demands = demands.filter(municipality=party.municipality)
        cat.check = len(
            DemandAnswer.objects.filter(
                party=party, agree_with_demand__isnull=False, demand__workgroup=cat
            )
        ) == len(demands)

    next = WorkGroup.objects.filter(election=election).order_by("id").first().id

    return render(
        request,
        "stranke/navodila.html",
        context={
            "categories": categories,
            "category_id": "navodila",
            "election_slug": election_slug,
            "next": next,
        },
    )


@login_required
def party_finish(request, election_slug=None):

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if election_slug is None:
        election = Election.objects.first()
    else:
        election = Election.objects.get(slug=election_slug)

    if party.finished_quiz:
        return redirect(f"/{election.slug}/kandidati_ke/povzetek")

    categories = WorkGroup.objects.filter(election=election).order_by("id")
    for cat in categories:
        demands = Demand.objects.filter(workgroup=cat, election=election)
        if party.municipality:
            demands = demands.filter(municipality=party.municipality)
        cat.check = len(
            DemandAnswer.objects.filter(
                party=party, agree_with_demand__isnull=False, demand__workgroup=cat
            )
        ) == len(demands)

    demands = Demand.objects.filter(election=election)
    if party.municipality:
        demands = demands.filter(municipality=party.municipality)
    allow_submit = len(
        DemandAnswer.objects.filter(party=party, agree_with_demand__isnull=False)
    ) == len(demands)
    finished_quiz = party.finished_quiz

    return render(
        request,
        "stranke/zakljucek.html",
        context={
            "categories": categories,
            "category_id": "zakljucek",
            "allow_submit": allow_submit,
            "finished_quiz": finished_quiz,
            "election_slug": election_slug,
        },
    )


@login_required
def party_save(request, election_slug=None):

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if election_slug is None:
        election = Election.objects.first()
    else:
        election = Election.objects.get(slug=election_slug)

    party.finished_quiz = True
    party.save()

    return redirect(f"/{election.slug}/kandidati_ke/povzetek")


@login_required
def party_summary(request, election_slug=None):

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if election_slug is None:
        election = Election.objects.first()
    else:
        election = Election.objects.get(slug=election_slug)

    party = Party.objects.get(user=request.user)

    categories = WorkGroup.objects.filter(election=election).order_by("id")

    answers_by_workgroup = []

    party_answers = DemandAnswer.objects.filter(party=party)

    for category in categories:
        demands = Demand.objects.filter(workgroup=category)
        if party.municipality:
            demands = demands.filter(municipality=party.municipality)
        answers = party_answers.filter(demand__in=demands)
        answers_by_workgroup.append({"workgroup": category.name, "answers": answers})

    return render(
        request,
        "stranke/povzetek.html",
        context={"answers_by_workgroup": answers_by_workgroup},
    )


def open_party_summary(request, election_slug=None, party_id=None):

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(id=party_id)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if election_slug is None:
        election = Election.objects.first()
    else:
        election = Election.objects.get(slug=election_slug)

    # party = Party.objects.get(user=request.user)

    categories = WorkGroup.objects.filter(election=election).order_by("id")

    answers_by_workgroup = []

    party_answers = DemandAnswer.objects.filter(party=party)

    for category in categories:
        demands = Demand.objects.filter(workgroup=category)
        if party.municipality:
            demands = demands.filter(municipality=party.municipality)
        answers = party_answers.filter(demand__in=demands)
        answers_by_workgroup.append({"workgroup": category.name, "answers": answers})

    return render(
        request,
        "stranke/open_povzetek.html",
        context={"answers_by_workgroup": answers_by_workgroup, "party": party},
    )


def verify_email(request, token):
    verification = get_object_or_404(EmailVerification, verification_key=token)
    user = verification.user
    user.is_active = True
    user.save()
    login(request, user)
    return redirect("/")


class Registracija(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "registration/registration.html", context={"form": form})

    def post(self, request):
        username = request.POST.get("email")
        password = request.POST.get("password")
        newsletter_permission = request.POST.get("newsletter_permission", False)
        redirect_path = request.META.get("HTTP_REFERER", "/")

        # try logging the user in
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(redirect_path)

        user = User.objects.create_user(
            username, email=username, password=password, is_active=False
        )
        Newsletter(
            user=user, permission=True if newsletter_permission == "on" else False
        ).save()
        # TODO send verification email
        return redirect("/hvala/")


class RestorePasswordView(View):
    def get(self, request, parameter=None):
        if parameter:
            form = RestorePasswordForm()
            return render(
                request, "registration/reset_password.html", context={"form": form}
            )
        else:
            form = RequestRestorePasswordForm()
            return render(
                request,
                "registration/request_reset_password.html",
                context={"form": form},
            )

    def post(self, request, parameter=None):
        if parameter:
            restore_password = get_object_or_404(ResetPassword, key=parameter)
            password = request.POST.get("password")
            user = restore_password.user
            user.set_password(password)
            user.save()
            return redirect("/")
        else:
            email = request.POST.get("email")
            user = get_object_or_404(User, email=email)
            ResetPassword(user=user).save()
            return redirect("/")


class MunicipalitiesList(APIView):
    def get(self, request, format=None):
        municipalities = Municipality.objects.all()
        municipality_serializer = MunicipalitySerializer(municipalities, many=True)
        return Response({"municipalities": municipality_serializer.data})


class MissingPartiesList(APIView):
    # @method_decorator(cache_page(60 * 60 * 24 * 40))
    def get(self, request, format=None, election_id=None, municipality_slug=""):
        try:
            municipality = Municipality.objects.get(slug=municipality_slug)
            parties = Party.objects.filter(
                election=election_id, municipality=municipality, finished_quiz=False
            )
        except Municipality.DoesNotExist:
            parties = Party.objects.filter(election=election_id, finished_quiz=False)

        party_serializer = PartySerializer(parties, many=True)

        return Response({"missing-parties": party_serializer.data})


class Volitvomat(APIView):
    @staticmethod
    def twist_answers(answers):
        return {key: not answers[key] for key in answers.keys()}

    # @method_decorator(cache_page(60 * 60 * 24 * 40))
    def get(self, request, format=None, election_id=None, municipality_id=""):

        if election_id is None:  # po defaultu se uporabi državnozborske
            election = Election.objects.first()
        else:
            election = Election.objects.get(id=election_id)

        try:
            if municipality_id:
                municipality = Municipality.objects.get(slug=municipality_id)
                parties = Party.objects.filter(
                    election=election, municipality=municipality, finished_quiz=True
                )
                demands = municipality.demands.all()
            else:
                raise Exception("Municipality id missing.")
        except:
            parties = Party.objects.filter(election=election, finished_quiz=True)
            demands = Demand.objects.filter(election=election)

        questions = {}

        for question in demands:
            demand_title = question.title
            demand_description = question.description
            party_answers = {}
            party_comments = {}
            for party in parties:
                # print(party)
                # print(question)
                try:
                    answer = DemandAnswer.objects.get(party=party, demand=question)
                    party_answers[party.id] = answer.agree_with_demand
                    party_comments[party.id] = DemandAnswer.objects.get(
                        party=party, demand=question
                    ).comment
                except:
                    party_answers[party.id] = None

            category = question.workgroup.id if question.workgroup else None

            questions[question.id] = {
                "demand_title": demand_title,
                "demand_description": demand_description,
                "party_answers": party_answers,
                "party_comments": party_comments,
                "category": category,
            }

        # municipalities = Municipality.objects.all()

        party_serializer = PartySerializer(parties, many=True)
        # municipality_serializer = MunicipalitySerializer(municipalities, many=True)

        return Response(
            {
                "questions": questions,
                "parties": party_serializer.data,
                # "municipalities": municipality_serializer.data
            }
        )


class QuestionsByMunicipalities(APIView):
    def get(self, request):
        election_id = request.query_params.get("election_id", None)
        question_ids = request.query_params.get("question_ids", None)
        winners_only = request.query_params.get("winners_only", False)

        try:
            # print("id", election_id)
            election = Election.objects.get(id=election_id)
            # print("election", election)
        except Election.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            demand_ids = question_ids.split(",") if question_ids else []
            demands = Demand.objects.filter(id__in=demand_ids, election=election)
            # print(demands)
        except Demand.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if winners_only:
            parties = Party.objects.filter(election=election, is_winner=True)
        else:
            parties = Party.objects.filter(election=election)
        # print(parties)
        # demands = Demand.objects.filter(election=election, municipality=municipality)
        answered_parties = []

        questions = {}

        for question in demands:
            demand_title = question.title
            demand_description = question.description
            party_answers = {}
            # party_comments = {}
            for party in parties:
                # print(party)
                # print(question)
                try:
                    answer = DemandAnswer.objects.get(party=party, demand=question)
                    party_answers[party.id] = answer.agree_with_demand
                    answered_parties.append(party)
                    # party_comments[party.id] = DemandAnswer.objects.get(party=party, demand=question).comment
                except:
                    pass
                    # party_answers[party.id] = None

            category = question.workgroup.id if question.workgroup else None

            questions[question.id] = {
                "demand_title": demand_title,
                "demand_description": demand_description,
                "party_answers": party_answers,
                # "party_comments": party_comments,
                "category": category,
            }

        municipalities = Municipality.objects.all()

        party_serializer = PartySerializer(answered_parties, many=True)
        municipality_serializer = MunicipalitySerializer(municipalities, many=True)

        return Response(
            {
                "questions": questions,
                "parties": party_serializer.data,
                "municipalities": municipality_serializer.data,
            }
        )
