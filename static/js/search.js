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

			})

		}
	})

})