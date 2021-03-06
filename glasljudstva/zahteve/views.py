from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponseNotFound
from django.contrib.auth import authenticate, login
from django import forms
from django.core.exceptions import PermissionDenied, BadRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib import messages

from zahteve.models import (
    WorkGroup,
    Demand,
    EmailVerification,
    ResetPassword,
    Newsletter,
    Party,
    DemandAnswer,
)
from zahteve.forms import (
    RegisterForm, 
    RestorePasswordForm, 
    RequestRestorePasswordForm, 
    DemandAnswerForm, 
    VoterQuestionForm,
)
from zahteve.serializers import PartySerializer
from zahteve.math import calculate_most_controversial_demands

# Create your views here.
def after_registration(request):
    return render(request, "registration/thank_you.html")


def landing(request):
    question_form_thankyou = False
    work_groups = WorkGroup.objects.all().order_by("?")
    parties = Party.objects.filter(finished_quiz=True).order_by("?")

    if request.method == 'POST':
        voter_question_form = VoterQuestionForm(request.POST)
        if voter_question_form.is_valid():
            question_form_thankyou = True
            voter_question_form.save()
            voter_question_form = VoterQuestionForm()
            messages.success(request, 'Hvala za oddano vprašanje!')
            return redirect("/")
        else:
            messages.error(request, 'Prišlo je do napake.')
    else:
        voter_question_form = VoterQuestionForm()
    
    return render(
        request,
        "zahteve/landing.html",
        context={
            "work_groups": work_groups, 
            "parties": parties, 
            "voter_question_form": voter_question_form,
            "question_form_thankyou": question_form_thankyou
        },
    )


def delovna_skupina(request, delovna_skupina_id):
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


def demand(request, demand_id):
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


def demands_party(request, party_id):
    # form = RegisterForm()
    try:
        party = Party.objects.get(id=party_id)
    except Party.DoesNotExist:
        return HttpResponseNotFound()

    work_groups = WorkGroup.objects.all().order_by("?")

    return render(
        request,
        "zahteve/stranka.html",
        context={
            "party": party,
            "work_groups": work_groups
            # 'form': form
        },
    )

def faq(request):
    return render(request, "zahteve/pogosta_vprasanja.html")


@login_required
def party(request):
    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if party.finished_quiz:
        return redirect("/stranke/povzetek")
    else:
        return redirect("/stranke/navodila")


class PartyDemand(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, category_id):
        # if user is not a party, restrict access
        try:
            party = Party.objects.get(user=request.user)
        except:
            raise PermissionDenied
        # ---------------------------------------

        if party.finished_quiz:
            return redirect("/stranke/povzetek")

        # for sidebar menu
        categories = WorkGroup.objects.all().order_by("id")
        for cat in categories:
            cat.check = len(
                DemandAnswer.objects.filter(
                    party=party, agree_with_demand__isnull=False, demand__workgroup=cat
                )
            ) == len(Demand.objects.filter(workgroup=cat))

        category = WorkGroup.objects.get(pk=category_id)
        demands = Demand.objects.filter(workgroup=category).order_by("id")

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
            },
        )

    def post(self, request, category_id):

        # if user is not a party, restrict access
        try:
            party = Party.objects.get(user=request.user)
        except:
            raise PermissionDenied
        # ---------------------------------------

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
            return redirect(f"/stranke/{next.id}")
        else:
            return redirect("/stranke/oddaja")


@login_required
def party_instructions(request):

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if party.finished_quiz:
        return redirect("/stranke/povzetek")

    categories = WorkGroup.objects.all().order_by("id")
    for cat in categories:
        cat.check = len(
            DemandAnswer.objects.filter(
                party=party, agree_with_demand__isnull=False, demand__workgroup=cat
            )
        ) == len(Demand.objects.filter(workgroup=cat))

    next = WorkGroup.objects.all().order_by("id").first().id

    return render(
        request,
        "stranke/navodila.html",
        context={"categories": categories, "category_id": "navodila", "next": next},
    )


@login_required
def party_finish(request):

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if party.finished_quiz:
        return redirect("/stranke/povzetek")

    categories = WorkGroup.objects.all().order_by("id")
    for cat in categories:
        cat.check = len(
            DemandAnswer.objects.filter(
                party=party, agree_with_demand__isnull=False, demand__workgroup=cat
            )
        ) == len(Demand.objects.filter(workgroup=cat))

    allow_submit = len(
        DemandAnswer.objects.filter(party=party, agree_with_demand__isnull=False)
    ) == len(Demand.objects.all())
    finished_quiz = party.finished_quiz

    return render(
        request,
        "stranke/zakljucek.html",
        context={
            "categories": categories,
            "category_id": "zakljucek",
            "allow_submit": allow_submit,
            "finished_quiz": finished_quiz,
        },
    )


@login_required
def party_save(request):

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    party.finished_quiz = True
    party.save()

    return redirect("/stranke/povzetek")


@login_required
def party_summary(request):

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    party = Party.objects.get(user=request.user)

    categories = WorkGroup.objects.all().order_by("id")

    answers_by_workgroup = []

    party_answers = DemandAnswer.objects.filter(party=party)

    for category in categories:
        demands = Demand.objects.filter(workgroup=category)
        answers = party_answers.filter(demand__in=demands)
        answers_by_workgroup.append({"workgroup": category.name, "answers": answers})

    return render(
        request,
        "stranke/povzetek.html",
        context={"answers_by_workgroup": answers_by_workgroup},
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


class Volitvomat(APIView):
    @staticmethod
    def twist_answers(answers):
        return {key: not answers[key] for key in answers.keys()}

    @method_decorator(cache_page(60 * 60 * 24 * 40))
    def get(self, request, format=None):
        parties = Party.objects.filter(finished_quiz=True)

        demands = Demand.objects.filter(
            id__in=list(calculate_most_controversial_demands(40).keys()) + [128]
        ).order_by("?")
        questions = {
            question.id: {
                "demand_title": question.title,
                "demand_description": question.description,
                "party_answers": {
                    party.id: DemandAnswer.objects.get(
                        party=party, demand=question
                    ).agree_with_demand
                    for party in parties
                },
                "party_comments": {
                    party.id: DemandAnswer.objects.get(
                        party=party, demand=question
                    ).comment
                    for party in parties
                },
                "category": question.workgroup.id,
            }
            for question in demands
        }
        # # palestina twist
        # questions[112]["twisted"] = {
        #     "demand_title": "SLOVENIJA NAJ NE PRIZNA SAMOSTOJNE PALESTINE.",
        #     "demand_description": "Slovenija ne sme priznati samostojnosti Palestine in naj ne obsoja okupacijskih praks Izraela.",
        #     "party_answers": self.twist_answers(questions[112]["party_answers"]),
        #     "party_comments": questions[112]["party_comments"],
        #     "category": questions[112]["category"],
        # }

        # # oploditev twist
        # questions[173]["twisted"] = {
        #     "demand_title": "SAMSKIM OSEBAM IN OSEBAM V ISTOSPOLNIH PARTNERSKIH ZVEZAH SE NE SME OMOGOČITI ENAKEGA DOSTOPA DO OPLODITVE Z BIOMEDICINSKO POMOČJO IN POSVOJITEV.",
        #     "demand_description": "Na podlagi ustavno varovane pravice do svobodnega odločanja o rojstvu otrok so z zakonom opredeljeni zdravstveni ukrepi, s katerimi se ženski in moškemu pomaga pri spočetju otroka. Te pravice se ne sme priznati samskim ženskam in ženskam v istospolnih partnerskih zvezah. Prav tako se pravice do posvojitve ne sme priznati samskim osebam in osebam v istospolnih partnerskih zvezah.",
        #     "party_answers": self.twist_answers(questions[112]["party_answers"]),
        #     "party_comments": questions[112]["party_comments"],
        #     "category": questions[112]["category"],
        # }

        # # javne finance twist
        # questions[238]["twisted"] = {
        #     "demand_title": "JAVNE FINANCE JE TREBA URAVNOTEŽITI Z VARČEVALNIMI UKREPI.",
        #     "demand_description": "Uravnoteženje javnih financ je treba dosegati z varčevalnimi ukrepi, čeprav varčevanje, ki ga spodbuja fiskalna konsolidacija, povečuje revščino in neenakost ter spodkopava doseganje ekonomskih in socialnih pravic. Varčevalni ukrepi so nujni, četudi gre za degradacijo javnih storitev in se ob tem ne spoštuje trajnostnega, vključujočega in pravičnega okrevanja.",
        #     "party_answers": self.twist_answers(questions[112]["party_answers"]),
        #     "party_comments": questions[112]["party_comments"],
        #     "category": questions[112]["category"],
        # }
        serializer = PartySerializer(parties, many=True)
        return Response({"questions": questions, "parties": serializer.data})
