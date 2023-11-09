let submittedAudio;
let submittedAudioBlob;
let submittedAudioUrl;
let $audio;
let $self;
let $instructions;

function handlerFunction(stream) {
  rec = new MediaRecorder(stream);
  rec.ondataavailable = e => {
    audioChunks.push(e.data);
    if (rec.state == "inactive") {
      submittedAudioBlob = new Blob(audioChunks, {
        type: 'audio/mpeg-3'
      });
      submittedAudioUrl = URL.createObjectURL(submittedAudioBlob);
    }
  }
}

function sendData(data, demandId) {
  var form = new FormData();
  form.append('file', data, 'data.mp3');
  form.append('title', 'data.mp3');
  //Chrome inspector shows that the post data includes a file and a title.
  $.ajax({
    type: 'POST',
    url: `/save-recording/${demandId}`,
    data: form,
    cache: false,
    processData: false,
    contentType: false
  }).done(function (data) {
    console.log(data);
    $self.fadeOut(300);
    $self.siblings('.repeat, .publish').fadeOut(300);
    $instructions.fadeIn(300).html('Tvoj glas bo slišan kmalu.').css({
      right: 0,
      left: 0,
      top: '56px',
      position: 'relative',
      margin: 'auto',
      'text-align': 'center',
    });
  });
}

function startRecording() {
  // Set audiochunks to an empty array and start recording
  audioChunks = [];
  rec.start();

  animateRecord($self, false);

  // Set timeout to stop recording after three seconds
  window.setTimeout(function () {
    rec.stop();
    animateRecord($self, true);

    // Make publish and repeat buttons visible
    $self.siblings('.publish, .repeat').css({
      visibility: 'visible',
    });

    // Update the button icon
    $self.children('.start-recording-svg').css({
      display: 'none',
    });
    $self.children('.play-svg').css({
      display: 'block',
    });
  }, 6000);

  // Fade out instructions
  $instructions.fadeOut(
    300,
    function () {
      $instructions.removeClass(
        'longtext'
      );
    });

  // Set new button icon, update classes and set new behaviour
  $self.animate({
      'right': `${($self.parent().width() / 2) - 15}px`,
    },
    300
  ).addClass(
    'start-recording'
  ).removeClass(
    'record'
  ).off(
    'click'
  ).on('click', function () {
    submittedAudio = new Audio(submittedAudioUrl);
    submittedAudio.play();
    animatePlay($self, false);
    // start listening for audio ended event
    submittedAudio.onended = function () {
      animatePlay($self, true);
    };
  });

  // Set publish event
  $self.siblings('.publish').on('click', function () {
    sendData(submittedAudioBlob, $self.data('demand-id'));
  });
  // Set repeat event
  $self.siblings('.repeat').on('click', function () {
    $self.siblings('.publish, .repeat').css({
      visibility: 'hidden',
    });
    beforePermissions();
  });

  $self.children('.record-svg').css({
    display: 'none',
  });
  $self.children('.start-recording-svg').css({
    display: 'block',
  });
}

function beforePermissions() {
  // ASK FOR MICROPHONE PERMISSION
  navigator
    .mediaDevices
    .getUserMedia({
      audio: true
    })
    .then(stream => {
      // We have permission, handle the microphone stream
      handlerFunction(stream)

      // Update instructions text
      $instructions.fadeIn(
        300
      ).html(
        'Pritisni gumb za<br />snemanje in naglas<br />ter odločno preberi<br />izbrano zahtevo.'
      ).addClass('longtext');

      // Change icon image, update classes and click event
      $self.animate({
          'right': `28px`,
        },
        300
      ).addClass(
        'record'
      ).removeClass(
        'want-to-record'
      ).off(
        'click'
      ).on(
        'click',
        startRecording
      );

      $self.children('.i-want-to-record-svg').css({
        display: 'none',
      });
      $self.children('.play-svg').css({
        display: 'none',
      });
      $self.children('.record-svg').css({
        display: 'block',
      });
    });
}

function onAudioEnd() {
  // Stop animation
  animatePlay($self, true);
  // Set instructions text
  $instructions.html(
    'DODAJ SVOJ<br />GLAS'
  ).fadeIn(
    300
  );

  // Animate the icon back right
  // Change the icon image and update classes
  $self.animate({
      'right': `28px`,
    },
    300
  ).addClass(
    'want-to-record'
  ).removeClass(
    'play'
  ).off(
    'click'
  ).on(
    'click',
    beforePermissions
  );

  $self.children('.play-svg').css({
    display: 'none',
  });
  $self.children('.i-want-to-record-svg').css({
    display: 'block',
  });
}

// Set first click on play buttons
$('.play').on('click', function (event) {
  // Set self
  $self = $(event.target);
  // Set instructions
  $instructions = $self.siblings('.instructions');
  // Set audio
  $audio = $self.siblings('audio');

  // Fade out instructions
  $instructions.fadeOut(300, function () {
    $audio[0].play();
  });

  // Move play icon to the middle
  $self.animate({
    'right': `${($self.parent().width() / 2) - 15}px`,
  }, 300);

  animatePlay($self, false);

  // start listening for audio ended event
  $audio[0].onended = onAudioEnd;
});

let animationTimer;
let animationWaves;
let animationCounter = 0;

function animatePlay($target, stop) {
  if (stop) {
    // STOP ANIMATION
    window.clearInterval(animationTimer);
    animationWaves.css({
      stroke: '#231f20',
    });
    animationCounter = 0;
  } else {
    animationWaves = $($target.find('.cls-1').get().reverse());
    animationWaves.css({
      stroke: 'none',
    });
    animationTimer = window.setInterval(function () {
      currentElement = $(animationWaves[animationCounter % animationWaves.length])
      currentElement.css({
        stroke: '#231f20',
      });
      if (animationCounter > 0) {
        previousElement = $(animationWaves[(animationCounter - 1) % animationWaves.length])
        previousElement.css({
          stroke: 'none',
        });
      }
      animationCounter += 1;
    }, 150);
  }
}

function animateRecord($target, stop) {
  console.log($target);
  if (stop) {
    // STOP ANIMATION
    window.clearInterval(animationTimer);
    animationWaves.css({
      stroke: '#231f20',
    });
    animationCounter = 0;
  } else {
    animationWaves = $($target.find('.start-recording-svg .cls-3-black').get());

    animationWaves.css({
      stroke: 'none',
    });

    animationTimer = window.setInterval(function () {
      if (animationCounter % 2 !== 0) {
        $(animationWaves[0]).css({
          stroke: '#231f20',
        });
        $(animationWaves[2]).css({
          stroke: '#231f20',
        });

        $(animationWaves[1]).css({
          stroke: 'none',
        });
        $(animationWaves[3]).css({
          stroke: 'none',
        });
      } else {
        $(animationWaves[1]).css({
          stroke: '#231f20',
        });
        $(animationWaves[3]).css({
          stroke: '#231f20',
        });

        $(animationWaves[0]).css({
          stroke: 'none',
        });
        $(animationWaves[2]).css({
          stroke: 'none',
        });
      }
      animationCounter += 1;
    }, 150);
  }
}

$('#submit-email').on('click', function () {
  fetch("https://podpri.lb.djnd.si/api/subscribe/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: $('#email').val(),
        segment_id: 10,
      }),
    })
    .then((res) => {
      if (res.ok) {
        return res.text();
      }
      throw new Error("Response not ok");
    })
    .then((res) => {
      alert('Hvala za prijavo!')
    })
    .catch((error) => {
      alert('Ups, nekaj je šlo narobe. :( Če se napaka ne odpravi sama, pošlji mail na vsi@danesjenovdan.si.')
    });
});

function party_quiz_radio_click(myRadio) {
  if (myRadio.value == "True") {
    $(myRadio).parents(".demand-answer-form").find(".form-comment").addClass("hidden")
  } else {
    $(myRadio).parents(".demand-answer-form").find(".form-comment").removeClass("hidden")
  }
}

const initialFormValues = {}
let submitted = false;

$('.demand-quiz-form').submit(function( event ) {
  submitted = true  
});

$( document ).ready(function() {
  // on ready save all field values
  // if we are on a page with the form that needs checking
  if ($('.demand-quiz-form').length > 0) {

    // save values
    $('.demand-quiz-form').find('input[type="radio"]').each(function() {
      initialFormValues[$(this).attr('id')] = $(this).is(':checked')
    });
    $('.demand-quiz-form').find('textarea').each(function() {
      initialFormValues[$(this).attr('id')] = $(this).val()
    });

    // add event listener to warn before leaving page
    window.addEventListener("beforeunload", (e) => {
      if (submitted) {
        return;
      }

      let isDirty = false;

      $('.demand-quiz-form').find('input[type="radio"]').each(function() {
        if (initialFormValues[$(this).attr('id')] != $(this).is(':checked')) {
          isDirty = true;
          return;
        }
      });

      $('.demand-quiz-form').find('textarea').each(function() {
        if (!$(this).parent().hasClass('hidden')) {
          if (initialFormValues[$(this).attr('id')] != $(this).val()) {
            isDirty = true;
            return;
          }
        }
      });

      if (isDirty) {
        e.returnValue = true;
        return true
      }
    });
  }
});