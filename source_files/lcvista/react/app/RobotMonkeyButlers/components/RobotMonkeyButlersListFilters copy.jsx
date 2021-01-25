import React, { Component } from 'react'
import { reduxForm, Field } from 'redux-form'
import PropTypes from 'prop-types'

import FormGroup from '~/Forms/components/FormGroup'

class Filters extends Component {
	static propTypes = {
		filterValues: PropTypes.object.isRequired,
		form: PropTypes.string.isRequired,
		initialValues: PropTypes.object.isRequired,
		onFilterChange: PropTypes.func.isRequired,
	}

	render() {
		const {
			filterValues,
			onFilterChange,
		} = this.props

		return (
			<div>
				<div className="hidden-print">
					<div className="row m-b-half">
						<Field
							className="form-control"
							component={FormGroup}
							inputComponent="input"
							name="search"
							onChangeHook={onFilterChange}
							placeholder="Search by name…"
							type="search"
							wrapperClassName="col-xs-12 col-lg-7"
						/>
					</div>
				</div>

				<div className="visible-print-block m-b-1">
					{filterValues && filterValues.search && (
						<p className="m-b-0"><strong>Search term:</strong> {filterValues.search}</p>
					)}
				</div>
			</div>
		)
	}
}


export default reduxForm({
	enableReinitialize: true,
})(Filters)
//Created by Robot.Monkey.Butler MONKEY_DATE
