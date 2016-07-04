$("#studentSurvey").on("submit", function(e) {
    e.preventDefault();
    data = getFormData(this);
    Form = this;
    $.ajax({
        cache : false,
        url : "/api",
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
