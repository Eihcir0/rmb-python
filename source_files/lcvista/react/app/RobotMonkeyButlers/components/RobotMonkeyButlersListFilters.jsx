import React, { Component, Fragment } from 'react'
import { reduxForm, Field } from 'redux-form'
import PropTypes from 'prop-types'

import R from 'ramda'

import FormGroup from '~/Forms/components/FormGroup'
import Select from '~/Forms/components/Select'
import CollapsibleContainer from '~/Shared/containers/CollapsibleContainer'


const exampleChoices = [['a', 'Option A'], ['b', 'Option B'], ['c', 'Option C']]


class RobotMonkeyButlersListFilters__Unconnected extends Component {
	static propTypes = {
		onFilterChange: PropTypes.func.isRequired,
		form: PropTypes.string.isRequired,
		initialValues: PropTypes.object.isRequired,
		currentFilterValues: PropTypes.object.isRequired,
	}

	render() {
		const {
			currentFilterValues,
			onFilterChange,
		} = this.props

		return (
			<Fragment>
				<div className="d-print-none">
					<CollapsibleContainer headerLabel="Available Filters" icon="filter">
						<div className="row">
							<div className="col-lg-3 col-md-6">
								<Field
									choices = {exampleChoices}
									className="form-control"
									component={FormGroup}
									inputComponent={Select}
									label="Filter by Option"
									name="option"
									onChangeHook={onFilterChange}
									required
								/>
							</div>
						</div>
					</CollapsibleContainer>
				</div>
				<div className="d-none d-print-block mb-1">
					{!R.isEmpty(currentFilterValues) && (
						<p className="mb-0"><strong>Filters selected:</strong></p>
					)}
					{R.prop('search', currentFilterValues) && (
						<p className="mb-0"><strong>Search Term:</strong> {currentFilterValues.search}</p>
					)}
					{R.prop('option', currentFilterValues) && (
						<p className="mb-0"><strong>Option:</strong> {currentFilterValues.option}</p>
					)}
				</div>
			</Fragment>
		)
	}
}

const wrappers = R.compose(
	reduxForm({ enableReinitialize: true }),
)

const RobotMonkeyButlersListFilters = wrappers(RobotMonkeyButlersListFilters__Unconnected)

export { RobotMonkeyButlersListFilters }