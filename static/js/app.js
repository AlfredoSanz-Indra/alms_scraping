
/**
 * 
 */
function click_btLaunchScriptPckgstate() {            
    console.log("Entering: click_btLaunchScriptPckgstate, domain:" + domain);

    const params = {};
    params['pckg_id_list'] = $('#pckgStateScriptForm #pckg_id_list').val();
    
    const mydomain = $('#mainform #mydomain').val();
    const theurl = mydomain + '/vf/ajx/scriptstate';
    console.log('->' + theurl);

    $.post(theurl, params, function(data) {            
        console.log('errormessage= ' + data['serverdata']['errormessage'] + ', successMessage=' + data['serverdata']['successMessage']);

        if('0' == data['serverdata']['errormessage']) {            
            const script_result = data['serverdata']['results'];        
            $('#response_area_script_pckg_state_inputs #thetext').html( data['serverdata']['inputs']);
            $('#response_area_script_pckg_state_results #thetext').html( data['serverdata']['results']);
        }
        else {
            console.log('Error Launching Package State Script, data:' + data['serverdata']['errormessage']);
            $('#response_area_script_pckg_state_results #thetext').html( data['serverdata']['errormessage']);
        }                
    });
}