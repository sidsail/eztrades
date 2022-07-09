const portfolio = {

	handleLogoutButtonClick: function () {

		$("#logout-button")[0].onclick = function (e) {

			console.log('logout button clicked');
			$(location).prop('href', '/logout');

		}

	},

	handleSessionButtonClick: function () {

		$("#session-button")[0].onclick = function (e) {

			console.log('session button clicked');
			$(location).prop('href', '/portfolio/session');

		}

	},

	displayEmail: function () {
		$.ajax({
			url: '/portfolio/session',
			method:'GET'

		}).done(function (resp) {
			const email = resp.profile.email;
			const given_name = resp.profile.given_name;
			console.log(email)
			$("#email-display")[0].innerHTML = "Hello, " + given_name;

		})

	},

}