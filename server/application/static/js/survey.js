$("#studentSurvey").on("submit", function(e) {
    e.preventDefault();
    let data = getFormData(this);
    let Form = this;
    let href = $(location).attr("href");

    $.ajax({
        cache : false,
        url : href,
        type : "POST",
        contentType : "application/json",
        dataType : "json",
        data : data,
        context : Form,
        success : function(result) {
            alert("Survey saved successfuly");
            window.location.href = "/surveyResults";
        },
        error : function(xhr, resp, text) {
            console.log(xhr, resp, text);
        }
    });
});
