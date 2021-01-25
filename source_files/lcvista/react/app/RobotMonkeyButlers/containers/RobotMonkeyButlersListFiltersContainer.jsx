import React, { Component } from 'react'
import { getFormValues } from 'redux-form'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { withRouter } from 'react-router'

import queryString from 'query-string'
import R from 'ramda'

import { RobotMonkeyButlersListFilters } from '~/RobotMonkeyButlers/components/RobotMonkeyButlersListFilters'
import { objectsWithTransactionsEqual } from '~/Models/helpers/Transaction'


class RobotMonkeyButlersListFiltersContainer__Unconnected extends Component {
	static propTypes = {
		formId: PropTypes.string.isRequired,
		// mstp:
		currentFilterValues: PropTypes.object.isRequired,
		initialFilterValues: PropTypes.object.isRequired,
	}

	shouldComponentUpdate(nextProps, nextState) {
		return !(
			objectsWithTransactionsEqual(this.props, nextProps) &&
			R.equals(this.state, nextState)
		)
	}

	handleFilterChange = (key, event) => {
		let value = event
		if (event && event.target) {
			value = event.target.value
		}

		const query = {
			...R.omit([key], queryString.parse(this.props.location.search)),
		}

		if (value) {
			query[key] = value
		}

		this.props.history.replace({
			...this.props.location,
			search: queryString.stringify(query),
		})
	}

	render() {
		const {
			currentFilterValues,
			formId,
			initialFilterValues,
		} = this.props

		return (
			<RobotMonkeyButlersListFilters
				currentFilterValues={currentFilterValues}
				form={formId}
				initialValues={initialFilterValues}
				onFilterChange={this.handleFilterChange}
			/>
		)
	}
}

const mapStateToProps = (state, { location, formId }) => {
	const currentFilterValues = getFormValues(formId)(state) || {}

	// This sets the initial value of the filter selectors based on the querystring
	const qs = queryString.parse(location.search)
	const initialFilterValues = R.isEmpty(qs) ? {} : qs

	return {
		currentFilterValues,
		initialFilterValues,
	}
}

const wrappers = R.compose(withRouter, connect(mapStateToProps, null))

const RobotMonkeyButlersListFiltersContainer = wrappers(RobotMonkeyButlersListFiltersContainer__Unconnected)

export { RobotMonkeyButlersListFiltersContainer }
