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

	handleTestInputButtonClick: function () {

		$("#test-input-submit")[0].onclick = function (e) {

			const ticker = $('#test-input-box')[0].value;
			if (ticker === "") {
				console.log('nothing')
				return 
			}
			console.log('submit button clicked')
			console.log(ticker)

			$.ajax({
				url: '/stock/data?ticker=' + ticker,
				method: 'GET'
			}).done(function (resp) {
				if (!resp.current_price) {
					console.log('not a valid ticker')
					return
				}
				console.log(resp)
				$("#stock-data")[0].innerHTML = resp.current_price
			} )

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
			$("#email-display")[0].innerHTML = "Hello, " + email;

		})

	},

	addStock: function () {

		$("#add-stock-button")[0].onclick = function (e) {

			const ticker = $('#test-input-box')[0].value;
			const count = 1

			$.ajax({
				url: '/addstock?ticker=' + ticker + '&count=' + count,
				method: 'POST'
			}).done(function(resp) {

				if (resp.success === true) {
					console.log('success')
				}
				if (resp.success === 'money') {
					console.log('not enough money')
				}
				if (resp.success === false) {
					console.log('failed')
				}

			})

		}

	}



}