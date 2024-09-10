// $('#document-name').on('input', function(){
    //     const doc_id = $(this).data('document-id')
    //     const newName = $(this).val()

    //     $.ajax({
    //         url: `{% url 'update_document_name' %}`,
    //         method: 'POST',
    //         data: {
    //             'id': doc_id,
    //             'name': newName,
    //             'csrfmiddlewaretoken': '{{csrf_token}}',
    //         },
    //         success: function(response){
    //             console.log('name updated');
    //         },
    //         error: function(response){
    //             console.log('name could not be updated');
    //         }
    //     });
    // });

    // $('#document-content').on('input',function(){
    //     const doc_id = $(this).data('document-id')
    //     const updatedContent = $(this).val()

    //     $.ajax({
    //         url: `{% url 'update_document_content' %}`,
    //         method: 'POST',
    //         data: {
    //             'id' :doc_id,
    //             'content': updatedContent,
    //             'csrfmiddlewaretoken': '{{csrf_token}}',
    //         },
    //          success: function (response) {
    //             console.log('Document content updated');
    //         },
    //         error: function (response) {
    //             console.log('Failed to update document content');
    //         }
    //     })
    // })


//     {% extends 'base.html' %}

// {% block title %}Edit Document | {{ document.name }}{% endblock %}

// {% block content %}
// <div class="p-10 lg:p-20">
//     <h1 class="text-3xl lg:text-6xl text-white">Edit Document</h1>

//     <input type="text" id="document-name" value="{{ document.name }}" placeholder="Document Name">
//     <textarea id="document-content">{{ document.content }}</textarea>
// </div>
// {% endblock %}

// {% block scripts %}
// <script>
//     const documentSlug = "{{ document.slug }}"; // Use slug instead of id
//     const ws_scheme = window.location.protocol === "https:" ? "wss://" : "ws://";
//     const socket = new WebSocket(ws_scheme + window.location.host + "/ws/documents/" + documentSlug + "/");

//     socket.onmessage = function(e) {
//         const data = JSON.parse(e.data);
//         const documentContent = data['document_content'];
//         document.getElementById('document-content').value = documentContent;
//     };

//     document.getElementById('document-content').addEventListener('input', function(e) {
//         const documentContent = e.target.value;
//         socket.send(JSON.stringify({
//             'document_content': documentContent
//         }));
//     });
// </script>
// {% endblock %}



    $(document).ready(function(){
        $('#document-name, #document-content').on('input', function(){
            var documentName = $('#document-name').val();
            var documentContent = $('#document-content').val();

            $.ajax({
                url: `{% url 'document_view' document.slug %}`,
                method: "POST",
                data: {
                    'name': documentName,
                    'content': documentContent,
                    'csrfmiddlewaretoken': '{{csrf_token}}',
                },
                 success: function (response) {
                    console.log('Document content updated');
                },
                error: function (response) {
                    console.log('Failed to update document content');
                }
            })
        })
    })
   