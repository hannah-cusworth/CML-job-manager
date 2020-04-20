function hide_checkbox(){
    var check_div = document.getElementById("checkbox");
    var check = document.getElementById("billing_address_select");
    var header = document.getElementById("billing_header");
    var status = "{{billing_status}}";
    
    if (status != "unbound"){
        check_div.style.display = "none";
    }
    if (status == "unused"){
        header.style.display = "none";
        check.checked = true; 
    }
    
    display_billing()
}
    
function display_billing(){
    var check = document.getElementById("billing_address_select");
    var billing = document.getElementById("billing_address_form");
    if (check.checked == false){
        billing.style.display = "block";
        
        document.getElementById("id_billing-line_one").required = true;
        document.getElementById("id_billing-city").required = true;
        document.getElementById("id_billing-county").required = true;
        document.getElementById("id_billing-postcode").required = true;
        
    }
    else {
        billing.style.display = "none";
        
        document.getElementById("id_billing-line_one").required = false;
        document.getElementById("id_billing-city").required = false;
        document.getElementById("id_billing-county").required = false;
        document.getElementById("id_billing-postcode").required = false;
    }
}