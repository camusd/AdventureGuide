$("#editSurvey").on("submit", function(e) {
    e.preventDefault();
    data = getFormData(this);
    Form = this;
    $.ajax({
        cache : false,
        url : "/api",
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
    $.ajax({
        cache : false,
        url : "../api/" + $.parseJSON(data)["_id"],
        type : "DELETE",
        success : function(result) {
            window.location.href = "/surveyResults";
        },
        error : function(xhr, resp, text) {
            console.log(xhr, resp, text);
        }
    });
});
