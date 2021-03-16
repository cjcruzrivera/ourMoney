function setFormValidation(id) {
    $(id).validate({
      highlight: function(element) {
        $(element).closest('.form-group').removeClass('has-success').addClass('has-danger');
        $(element).closest('.form-check').removeClass('has-success').addClass('has-danger');
      },
      success: function(element) {
        $(element).closest('.form-group').removeClass('has-danger').addClass('has-success');
        $(element).closest('.form-check').removeClass('has-danger').addClass('has-success');
      },
      errorPlacement: function(error, element) {
        $(element).closest('.form-group').append(error);
      },
      messages: {
          nombre: "Debe ingresar el nombre de la cuenta",
          tipo: "Debe seleccionar el tipo de cuenta",
          saldo: "Debe ingresar el saldo de la cuenta propia"
      },
    });
  }
