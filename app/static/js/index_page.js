const index = {

	handleLoginButton: function() {

		$("#login-button")[0].onclick = function (e) {

			console.log('login button clicked')
			$(location).prop('href', '/login')

		}

	}


}

window.index = index