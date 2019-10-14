$(document).ready(function() {
    $('#image_spinner').hide()
    $('#video_spinner').hide()
    $('#audio_spinner').hide()

    alertify.set('notifier', 'position', 'top-center');

    $(".custom-file-input").on("change", function() {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });
})


function checkImageInput() {
    var elementToCheck = document.getElementById("image_input")

    if (elementToCheck.files.length == 0) {
        elementToCheck.focus()
        alertify.warning("Please upload an image")
        return false
    }

    return true
}

function checkVideoInput() {
    var elementToCheck = document.getElementById("video_input")

    if (elementToCheck.files.length == 0) {
        elementToCheck.focus()
        alertify.warning("Please upload a video")
        return false
    }

    return true
}

function checkAudioInput() {
    var elementList = [
        document.getElementById("source_audio_input"),
        document.getElementById("target_audio_input")
    ]

    for (var i = 0; i < elementList.length; i++) {
        if (elementList[i].files.length == 0) {
            elementList[i].focus()
            alertify.warning("Please upload an audio")
            return false
        }
    }
    return true
}

function uploadImage() {
    if (!checkImageInput()) {
        return false
    }

    var form_data = new FormData($('#image-form')[0])

    $('#image_spinner').show()

    $.ajax({
        url: "/img_sr",
        type: "POST",
        cache: false,
        data: form_data,
        processData: false,
        contentType: false,
        success: function(result) {
            var image_form = document.getElementById("image-form")
            image_form.innerHTML = image_form.innerHTML + "<a class='btn btn-primary mt-2' href='/img_sr'>Download</button>"
            alertify.success("Finished!")
            $('#image_spinner').hide()
        },
        error: function(e) {
            console.log(e.status)
            alertify.error("Error occurred.");
            $('#image_spinner').hide()
        }
    })
}

function uploadVideo() {
    if (!checkVideoInput()) {
        return false
    }

    var form_data = new FormData($('#video-form')[0])

    $('#video_spinner').show()

    $.ajax({
        url: "/video_sr",
        type: "POST",
        cache: false,
        data: form_data,
        processData: false,
        contentType: false,
        success: function(result) {
            var video_form = document.getElementById("video-form")
            video_form.innerHTML = video_form.innerHTML + "<a class='btn btn-primary mt-2' href='/video_sr'>Download</button>"
            alertify.success("Finished!")
            $('#video_spinner').hide()
        },
        error: function(e) {
            console.log(e)
            alertify.error("Error occurred.");
            $('#video_spinner').hide()
        }
    })
}

function uploadAudio() {
    if (!checkAudioInput()) {
        return false
    }

    var form_data = new FormData($('#audio-form')[0])

    $('#audio_spinner').show()

    $.ajax({
        url: "/audio_st",
        type: "POST",
        cache: false,
        data: form_data,
        processData: false,
        contentType: false,
        success: function(result) {
            var audio_form = document.getElementById("audio-form")
            audio_form.innerHTML = audio_form.innerHTML + "<a class='btn btn-primary mt-2' href='/audio_st'>Download</button>"
            alertify.success("Finished!")
            $('#audio_spinner').hide()
        },
        error: function(e) {
            console.log(e.status)
            alertify.error("Error occurred.");
            $('#audio_spinner').hide()
        }
    })
}