function setFormValidation(id) {
    $(id).validate({
        highlight: function (element) {
            $(element).closest('.form-group').removeClass('has-success').addClass('has-danger');
            $(element).closest('.form-check').removeClass('has-success').addClass('has-danger');
        },
        success: function (element) {
            $(element).closest('.form-group').removeClass('has-danger').addClass('has-success');
            $(element).closest('.form-check').removeClass('has-danger').addClass('has-success');
        },
        errorPlacement: function (error, element) {
            $(element).closest('.form-group').append(error);
        },
        messages: {
            nombre: "Debe ingresar el nombre de la cuenta",
            tipo: "Debe seleccionar el tipo de cuenta",
            saldo: "Debe ingresar el saldo de la cuenta propia",
            origen: "Debe seleccionar la cuenta de origen",
            destino: "Debe seleccionar la cuenta de destino",
            total: "Debe ingresar el valor de la transacción",
            realiza: "Debe seleccionar quien realiza la transacción",
            fecha_realiza: "Debe seleccionar la fecha de la transacción",
        },
    });
}
