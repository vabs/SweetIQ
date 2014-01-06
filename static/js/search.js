var isDone = 0;
$(function(){
	$("#searchBtn").click(function(){
		var nam = $("#location").val();
		var phno = $("#phonenumber").val();
		var add = $("#address").val();
		if(nam == ''){
			$("#location").css("border", "2px solid red");
		}
		else if(add == ''){
			$("#location").css("border", "none");
			$("#address").css("border", "2px solid red");
		}
		else if(phno == ''){
			$("#address").css("border", "none");
			$("#location").css("border", "none");
			$("#phonenumber").css("border", "2px solid red");
		}
		else{
			$("#address").css("border", "none");
			$("#location").css("border", "none");
			$("#phonenumber").css("border", "none");
			$.ajax({
				type: "POST",
				url: "/find",
				data: { name: nam, address: add, phone: phno },
				success: function(sessionId){
					console.log(sessionId);
					poller(sessionId);
				}
			});
		}
	})

})

function isComplete(sId){
	$.blockUI({ message: '<h1>Searching for places</h1>' }); 
	$.ajax({
			url: "/isComplete/" + sId,
			success: function(res){
				isDone = res;
			}
		});
}

function poller(sId){
	isComplete(sId);
	if(parseInt(isDone) != 1 && parseInt(isDone) != -1){
                console.log( "Is done : " + isDone);
		setTimeout(function(){ poller(sId) }, 5000);
	}
	if(parseInt(isDone) == -1 ){
		$.get('/error');
	}
	else{
                console.log( "Is done : " + isDone);
		window.location.href = '/getData/'+ sId;
	}
}


