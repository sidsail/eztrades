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
			})

		}

	},

	displayEmail: function () {
		$.ajax({
			url: '/portfolio/session',
			method: 'GET'

		}).done(function (resp) {
			const email = resp.profile.email;
			const given_name = resp.profile.given_name;
			console.log(email)
			$("#email-display")[0].innerHTML = "Hello, " + email;

		})

	},

	handleAddStockButtonClick: function () {

		$("#add-stock-button")[0].onclick = function (e) {

			const ticker = $('#test-input-box')[0].value.toUpperCase().trim();
			const count = $('#count-input-box')[0].value.trim();

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
			}).done(function (resp) {
				console.log(resp)
				if ('error' in resp) {
					console.log(resp.error)
					return
				}
				if (resp.success === true) {
					console.log('successful!')
				}
				portfolio.updateBPDisplay(resp.new_money)
				console.log(resp.value)

				const values = document.getElementById("value-display")
				const current_value = values[0].value
				console.log(current_value)

			})

		}

	},

	handleSellStockButtonClick: function () {

		$('#sell-stock-button')[0].onclick = function (e) {

			const ticker = $('#test-input-box')[0].value.toUpperCase().trim();
			const count = $('#count-input-box')[0].value.trim();

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
					console.log(resp.error)
					return
				}

				portfolio.updateBPDisplay(resp.new_money)
				console.log(resp.value)

				current_value = ($('#value-display')[0].innerHTML)
				console.log(current_value)

				//new_value = current_value + resp.value

				//$('#value-display')[0].innerHTML = new_value

			})
		}

	},

	handleGetHoldingsButtonClick: function () {

		$('#get-holdings-button')[0].onclick = function (e) {

			$.ajax({
				url: '/portfolio/holdings',
				method: 'GET'
			}).done(function (resp) {

				Object.keys(resp).forEach(function (key) {

					console.log(key, resp[key])
				})

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
				for (let i = 0; i < transactions_arr.length; i++) {
					console.log(transactions_arr[i])
				}

			})
		}
	},

	updateBPDisplay: function (money) {

		$('#money-display')[0].innerHTML = 'buying power: ' + money.toString()
	},

	updatePortfolioValueDisplay: function (value) {

		$('#value-display')[0].innerHTML = 'portfolio value: ' + value.toString()
		const current_value = $('#value-display')[0].value;
		console.log(current_value)
	},


	displayPortfolioOnInitial: function () {

		$.ajax({
			url: '/portfolio/holdings',
			method: 'GET'
		}).done(function (resp) {

			portfolio.updateBPDisplay(resp.money)

			let value = 0
			Object.keys(resp).forEach(function (key) {

				if (key === 'money') {
					return
				}

				value += (resp[key]['current_price'] * resp[key]['count'])
				portfolio.updatePortfolioValueDisplay(value)

			})
		})

	},



}