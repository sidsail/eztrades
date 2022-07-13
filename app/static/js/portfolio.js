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

	handleAddStockButtonClick: function () {

		$("#add-stock-button")[0].onclick = function (e) {

			const ticker = $('#test-input-box')[0].value;
			const count = $('#count-input-box')[0].value;
			
			if (isNaN(count)) {
				console.log('not a number')
				return;
			}
			if (ticker === "") {
				return
			}

			$.ajax({
				url: '/portfolio/action?ticker=' + ticker + '&count=' + count + '&action=buy',
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

	},

	handleSellStockButtonClick: function () {

		$('#sell-stock-button')[0].onclick = function (e) {

			const ticker = $('#test-input-box')[0].value;
			const count = $('#count-input-box')[0].value;

			if (isNaN(count)) {
				console.log('not a number')
				return;
			}
			if (ticker === "") {
				return
			}

			$.ajax({
				url: '/portfolio/action?ticker=' + ticker + '&count=' + count + '&action=sell',
				method: 'POST'
			}).done(function (resp) {

				if (resp.success === true) {
					console.log('success')
				}

				if (resp.success === false) {
					console.log('dont have')
				}


			})
		}	

	},

	handleGetHoldingsButtonClick: function () {

		$('#get-holdings-button')[0].onclick = function (e) {

			$.ajax({
				url: '/portfolio/holdings',
				method: 'GET'
			})

		}

	},

	handleGetTransactionHistoryButtonClick: function () {

		$('#get-transaction-history')[0].onclick = function (e) {

			$.ajax({
				url: '/portfolio/transactions',
				method: 'GET'
			}).done(function (resp) {

				transactions_arr = resp.transactions
				for (let i=0; i < transactions_arr.length; i++) {
					console.log(transactions_arr[i])
				}

			})
		}
	}



}