// --- Javascript for Edit Icon Modal ---
        function edit_icon() {
            $('#edit_icon_modal').modal('show');
        }

        // Deal with input of icons
        $('#image_upload_input').on('change', function () {

            $('#placeholder_segment').hide();
            $('#preview_img').show();
            readURL(this);
        });

        // Library Code to Preview Image on Upload
        function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();

                reader.onload = function (e) {
                    $('#preview_img').attr('src', e.target.result);
                }
                reader.readAsDataURL(input.files[0]);
            }
        }