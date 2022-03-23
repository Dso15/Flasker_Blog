function create_form(content_text, csrf_token, message_id) {
    const message_body = document.getElementById('message-body-' + message_id); 
    const text = message_body.getElementsByTagName("p")[0];
    const text_to_edit = text.innerHTML

        
    // Create Form
    const form = document.createElement('form')
    form.setAttribute('method', "post")
    form.setAttribute('action', "/posts/quick-message-edit-" + message_id)


    // Replace text with Form
    text.replaceWith(form)


    // Create Form-CSRF Token Field
    const csrf_protection = document.createElement('input')
    csrf_protection.setAttribute('type', "hidden")
    csrf_protection.setAttribute('name', "csrf_token")
    csrf_protection.setAttribute('value', csrf_token)


    // Create Form-Content Label
    const content_label = document.createElement('label')
    content_label.setAttribute('class', "form-label text-light")
    content_label.setAttribute('for', "content")
    content_label.innerHTML = "Edit Message:"

    // Create Form-Content Field
    const content = document.createElement('textarea')
    content.setAttribute('style', "background-color: #c9c9c9;")
    content.setAttribute('class', "form-control mb-2")
    content.setAttribute('id', "content")
    content.setAttribute('name', "content")
    content.value = text_to_edit


    // Create Form-Submit Button
    const submit = document.createElement('button')
    submit.setAttribute('type', "submit")
    submit.setAttribute('class', "btn btn-secondary btn-sm mt-3")
    submit.innerHTML = "Save"
    

    // Append Form-Items to Form
    form.appendChild(csrf_protection)
    form.appendChild(content_label)
    form.appendChild(content)
    form.appendChild(submit)


    // Replace textarea with CKEDITOR
    CKEDITOR.replace(content)
};