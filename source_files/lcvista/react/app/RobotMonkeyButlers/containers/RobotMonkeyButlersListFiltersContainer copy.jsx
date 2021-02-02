import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { connect } from 'react-redux'
import { withRouter } from 'react-router'
import { getFormValues } from 'redux-form'

import R from 'ramda'
import Filters from '../components/RobotMonkeyButlersListFilters'

//(^_^)config:start(^_^)
const FORM_ID = 'RobotMonkeyButlersListFilters'
//(^_^)config:end(^_^)


class FiltersContainer extends Component {
	static propTypes = {
		// mstp:
		filterValues: PropTypes.object.isRequired,
		initialFilterValues: PropTypes.object.isRequired,
	}

	handleFilterChange = (key, event) => {
		let value = event
		if (event && event.target) {
			value = event.target.value
		}

		const query = {
			...R.omit([key],this.props.location.query),
		}

		if (value) {
			query[key] = value
		}
		this.props.router.replace({
			...this.props.location,
			query,
		})
	}

	render() {
		const {
			filterValues,
			initialFilterValues,
		} = this.props

		return (
			<Filters
				filterValues={filterValues}
				form={FORM_ID}
				initialValues={initialFilterValues}
				onFilterChange={this.handleFilterChange}
			/>
		)
	}
}

const mapStateToProps = (state, ownProps) => {
	const queryString = ownProps.location && ownProps.location.query || {}
	const filterValues = getFormValues(FORM_ID, state)

	// Set the initial filter values based on the querystring
	const initialFilterValues = R.isEmpty(queryString) ? {} : {
		...queryString,
	}

	return {
		filterValues,
		initialFilterValues,
	}

}

const wrappers = R.compose(
	withRouter,
	connect(mapStateToProps, null),
)


export default wrappers(FiltersContainer)
//Created by Robot.Monkey.Butler MONKEY_DATE
