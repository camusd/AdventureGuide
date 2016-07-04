function getFormData(form) {
    var data = {};
    var Form = form;
    $.each(form.elements, function(i, v) {
        var input = $(v);
        if (input.attr("type") == "radio") {
            if (input.is(":checked")) {
                data[input.attr("name")] = input.val();
            }
        } else if (input.attr("type") == "checkbox") {
            if (input.is(":checked")) {
                if (input.attr("name") in data) {
                    data[input.attr("name")].push(input.val());
                } else {
                    data[input.attr("name")] = [];
                    data[input.attr("name")].push(input.val());
                }
            }
        } else {
            data[input.attr("name")] = input.val();
        }
        delete data["undefined"];
    });
    return data = JSON.stringify(data);
}
