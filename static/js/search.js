$(function(){
	$("#searchBtn").click(function(){
		var name = $("#location").val()
		var phno = $("#phonenumber").val()
		var add = $("#address").val()
		if(name == ''){
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
			$.ajax(function(){
				url: '/find',
				data: {
					name: name,
					address: add,
					phone: phno
				},
				success: function(sessionId){
					console.log(sessionId)
					poller(sessionId)
				}
			})

		}
	})

})

function poller(sId){
	isComplete(sID);
	while(isDone != 1){
		setTimeout(isComplete(sId), 5000)
	}
	$.ajax(function(){
			url: '/getData/' + sId,
			data: {
				sessionId: sId
			},
			success: function(res){
				isDone = res
			}
		})
}

function isComplete(sId){
	$.ajax(function(){
			url: '/isComplete/' + sId,
			data: {
				name: name,
				address: add,
				phone: phno
			},
			success: function(res){
				isDone = res
			}
		})
}