import React, { Component, Fragment } from 'react'
import { getFormValues } from 'redux-form'
// import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { withRouter } from 'react-router'

import R from 'ramda'


// import { getAuthenticatedPerson, } from '~/Auth/selectors'

import { setSuccessAlert } from '~/Alerts/helpers'
import DeleteConfirmModal from '~/Shared/containers/DeleteConfirmModal'
import PaginatedTableContainer from '~/Shared/containers/PaginatedTableContainer'
import Transaction from '~/Models/helpers/Transaction'
import { bindActionCreators } from 'redux'
import * as modelActions from '~/Models/actions'

import RobotMonkeyButlersListTableRow from '~/RobotMonkeyButlers/components/RobotMonkeyButlersListTableRow'


//(^_^)config:start(^_^)
const ENDPOINT = 'robotmonkeybutlers'
const TABLE_COLUMNS = [['Name', 'name'], ['Management', undefined]]
//(^_^)config:end(^_^)



class RobotMonkeyButlersListContainer extends Component {

	static propTypes = {
		// organization: PropTypes.object.isRequired,
		// reportConfiguration: PropTypes.oneOfType([
		// 	PropTypes.bool,
		// 	PropTypes.object,
		// ]),
	}

	state = {
		proposedForDeletion: null,
	}

	handleDeleteRequest = (item) => {
		this.setState({ proposedForDeletion: item })
	}

	handleCancelDelete = () => {
		this.setState({ proposedForDeletion: null })
	}

	handleDelete = () => {
		const robotMonkeyButler = this.state.proposedForDeletion
		this.setState({ proposedForDeletion: null })
		this.props.actions.invalidateEndpoint('robotmonkeybutlers')
		setSuccessAlert(
			robotMonkeyButler.name,
			{
				verb: 'deleted',
			}
		)
	}

	render() {
		const {
			organizationSlug,
			tableColumns,
			paginatedTableTransaction,
		} = this.props

		const { proposedForDeletion } = this.state

		const handlers = [
			['Delete', this.handleDeleteRequest]
		]
		return (
			<Fragment>
				<PaginatedTableContainer
					columns={tableColumns}
					initialOrdering="name"
					location={location}
					rowComponent={RobotMonkeyButlersListTableRow}
					rowProps={{
						location,
						organizationSlug,
						handlers,
					}}
					tableKey="RobotMonkeyButlersListTable"
					transaction={paginatedTableTransaction}
				/>
				{proposedForDeletion && (
					<DeleteConfirmModal
						endpoint="robotmonkeybutlers"
						objectId={proposedForDeletion.id}
						onCancel={this.handleCancelDelete}
						onDelete={this.handleDelete}
					>
						<div className="p-a-1">
							<h5>
								Delete Robot Monkey Butler?
							</h5>
							<p>This action will delete{' '}
							<strong>
								{proposedForDeletion.name}.
							</strong></p>
							<p>This action cannot be undone.</p>
						</div>
					</DeleteConfirmModal>
				)}
			</Fragment>
		)
	}
}

const FORM_ID = 'RobotMonkeyButlersListFilters'  // Find a better way to do this -- pass down from scene?

const mapStateToProps = (state, { params: { organizationSlug } }) => {
	const filterValues = getFormValues(FORM_ID)(state) || {}

	// add filters from url
	const txnParams = {
		search: filterValues.search,
	}

	const paginatedTableTransaction = new Transaction(
		ENDPOINT,
		txnParams,
	)

	const tableColumns = TABLE_COLUMNS.reduce((acc, curr) => {
		acc.push({ label: curr[0], dataKey: curr[1]})
		return acc
	}, [])

	return {
		paginatedTableTransaction,
		tableColumns,
		organizationSlug,
	}
}

const mapDispatchToProps = (dispatch) => {
	return {
		actions: bindActionCreators(modelActions, dispatch),
	}
}


const wrappers = R.compose(
	withRouter,
	connect(mapStateToProps, mapDispatchToProps),
)

export default wrappers(RobotMonkeyButlersListContainer)

//Created by Robot.Monkey.Butler MONKEY_DATE