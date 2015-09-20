$(document).ready(function(){

	/* Link Event Handlers */
	$('#link_modules').click(function(){
		location.hash = "modules";
		$('.panel-title').html('<strong>Modules</strong><div class="btn-toolbar pull-right"><button href="javascript:void;" id="btn-add" class="btn-link">Add Module</button></div>');
		$('.homepage').addClass('hidden');
		$('.table-viewer').removeClass('hidden');
	});

	$('#link_users').click(function(){
		location.hash = "users";
		$('.panel-title').html('<strong>Users</strong><div class="btn-toolbar pull-right"><button href="javascript:void;" id="btn-add" class="btn-link">Add Users</button></div>');
		$('.homepage').addClass('hidden');
		$('.table-viewer').removeClass('hidden');
	});

	$('#link_devices').click(function(){
		location.hash = "devices";
		$('.panel-title').html('<strong>Devices</strong><div class="btn-toolbar pull-right"><button href="javascript:void;" id="btn-add" class="btn-link">Add Devices</button></div>');
		$('.homepage').addClass('hidden');
		$('.table-viewer').removeClass('hidden');
	});
	/* End Link Event Handlers */

	/* Hash Change Event Handler */
	$(window).on('hashchange', function(){
		if(location.hash.slice(1) != ""){
			HashProcessor(location.hash.slice(1));
		}
	}).trigger('hashchange');
	/* End Hash Change Event Handler */

	/* Table Buttons Event Handlers */
	$('#add').click(function(){
		$('#module_name_text').val("");
		$('#module_author_text').val("");
		$('#module_filename_text').val("");
		$('#module_priority_text').val("");
		$('#module_type_text').attr("placeholder", "user");
		$('#module_identifier_text').attr("placeholder", "");
		$('#model_identifier').addClass('hide');
		$('.modal-title').text("Add Module");
		$('#modal').modal('show');
	});

	$(document).on('click', '.module_disable', function(){
		$.ajax({
		    url: '/api/module/'+$(this).attr('data_id'),
		    type: 'POST',
		    success: function(result) {
		    	if(result == "Disabled" ){
		    		//alert("Module disabled");
		    	}
		    	else if(result == "Enabled"){
		    		//alert("Module enabled");
		    	}
		    	else{
		    		alert("Error. Module may not have changed state.");
		    	}

		    	//Destroying currrent table
				$('#table').dataTable().fnDestroy();

				//Rebuilding table
				InitDatatable();
			}
		});	
	});

	$(document).on('click', '.module_edit', function(){
		//Getting module info
		$.getJSON( "/api/module/"+$(this).attr('data_id'), function( data ) {
			
			//Setting values
			if(data[5] == 0){
				$('#module_status_value').val("Disabled");
			}
			else if(data[5] == 1){
				$('#module_status_value').val("Enabled");
			}
			$('.modal-title').text("Edit Module: "+data[1]);
			$('#module_name_text').val(data[1]);
			$('#module_author_text').val(data[6]);
			$('#module_filename_text').val(data[3]);
			$('#module_priority_text').val(data[4]);
			$('#module_type_text').attr("placeholder", data[2]);
			//$('#module_identifier_text').attr("placeholder", data[0]);
			$('#module_identifier_text').val(data[0]);
			$('#model_identifier').removeClass('hide');
		});

		$('#modal').modal('show');
	});

	$(document).on('click', '.module_export', function(){
		alert("Functionality coming soon!");
	});

	$('#module_save').click(function(){
		//Getting values of fields
		var module_name = $('#module_name_text').val();
		var module_author = $('#module_author_text').val();
		var module_filename = $('#module_filename_text').val();
		var module_priority = $('#module_priority_text').val();
		var module_status = $('#module_status_value').val();

		//Converting status into DB friendly format
		if(module_status == "Enabled"){
			var module_status = 1;
		}
		else if(module_status == "Disabled"){
			var module_status = 0;
		}
		
		//Checking if we are adding of editing
		if($('#model_identifier').hasClass('hide')){
			//Adding
			$.post( 
                  "/api/modules",
                  { name: module_name, author: module_author, filename: module_filename, status: module_status, priority: module_priority },
                  function(data) {
                     console.log(data);
                  }
               );
		}
		else{
			//Editing

			//Getting ID
			var module_id = $('#module_identifier_text').val();

			$.ajax({
			    url: "/api/modules",
			    type: 'PUT',
			    data: { name: module_name, author: module_author, filename: module_filename, status: module_status, priority: module_priority, id: module_id },
			    success: function(result) {
                	console.log(result);
            	}
			});

		}

		//Clearing modal
		ClearModal();

		//Hiding modal
		$('#modal').modal('hide');

	});

	/* End Table Buttons Event Handlers */
});

function HashProcessor(hash){
	//If table is initilized, destroy
	if($.fn.dataTable.isDataTable('#table')){
		$('#table').dataTable().fnDestroy();
	}

	$.getJSON( "/api/"+hash, function( data ) {
		//console.log(data)
			$('#table').dataTable({
		    "aaData": data,
		    "aoColumns": [
		        { "sTitle": "Title", "mData": 1 },
		        { "sTitle": "Status",  "mRender": function ( data, type, full ){
						if(full[5] == 0){
							return "Disabled"
						}
						else if (full[5] == 1){
							return "Enabled"
						}	        
		        	}
		        },
		        { "sTitle": "Priority", "mData": 4 },
		        { "sTitle": "Tools", "mRender": function ( data, type, full ) {
		        	if(full[5] == 0){
		        		return "<div class='btn-toolbar'><button class='btn btn-success module_edit' data_id='"+full[0]+"'>Edit</button><button class='btn btn-danger module_disable' data_id='"+full[0]+"'>Enable</button><button class='btn btn-default btn-info module_export' data_id='"+full[0]+"'>Export</button></div>"
		        	}
		        	else if(full[5] == 1){
	                    return "<div class='btn-toolbar'><button class='btn btn-success module_edit' data_id='"+full[0]+"'>Edit</button><button class='btn btn-danger module_disable' data_id='"+full[0]+"'>Disable</button><button class='btn btn-default btn-info module_export' data_id='"+full[0]+"'>Export</button></div>"
	                }
			}}],
			"order": [[ 2, "asc" ]]	
		});
	});
	
}

function ClearModal(){
	$('.modal-title').text("");
	$('#module_name_text').val("");
	$('#module_author_text').val("");
	$('#module_filename_text').val("");
	$('#module_priority_text').val("");
	$('#module_type_text').attr("placeholder", "");
	$('#module_identifier_text').val("");
	$('#model_identifier').removeClass('hide');
}