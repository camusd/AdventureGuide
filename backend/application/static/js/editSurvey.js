$("#editSurvey").on("submit", function(e) {
    e.preventDefault();
    let data = getFormData(this);
    let Form = this;
    let href = $(location).attr("href");

    $.ajax({
        cache : false,
        url : href,
        type : "PUT",
        contentType : "application/json",
        dataType : "json",
        data : data,
        context : Form,
        success : function(result) {
            window.location.href = "/surveyResults";
        },
        error : function(xhr, resp, text) {
            console.log(xhr, resp, text);
        }
    });
});

$("#deleteSurvey").on("submit", function(e) {
    e.preventDefault();
    data = getFormData(this);
    let href = $(location).attr("href");
    $.ajax({
        cache : false,
        url : href,
        type : "DELETE",
        success : function(result) {
            alert("Survey deleted successfuly");
            window.location.href = "/surveyResults";
        },
        error : function(xhr, resp, text) {
            console.log(xhr, resp, text);
        }
    });
});
