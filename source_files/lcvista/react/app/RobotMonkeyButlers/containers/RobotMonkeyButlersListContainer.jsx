import React, { Component, Fragment } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import queryString from 'query-string'
import { withRouter } from 'react-router-dom'

import R from 'ramda'

import { setSuccessAlert } from '~/Alerts/helpers'
import DeleteConfirmModal from '~/Shared/containers/DeleteConfirmModal'
import PaginatedTableContainer from '~/Shared/containers/PaginatedTableContainer'
import Transaction from '~/Models/helpers/Transaction'
import { bindActionCreators } from 'redux'
import * as modelActions from '~/Models/actions'

import { RobotMonkeyButlersListRow } from '~/RobotMonkeyButlers/components/RobotMonkeyButlersListRow'
import SearchField from '~/Shared/components/filterFields/SearchField'
import Card from '~/Shared/containers/Card'


class RobotMonkeyButlersListContainer__Unconnected extends Component {
	static propTypes = {
		formId: PropTypes.string.isRequired,

		//mstp:
		paginatedTableTxn: PropTypes.object.isRequired,
		searchValue: PropTypes.string,  // used for initialValues on search
	}

	static defaultProps = {
		tableColumns: [
			{ label:'Id', dataKey: 'id' },
			{ label:'' },
		],
		initialOrdering: '-id',
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
		const toDelete = this.state.proposedForDeletion
		this.setState({ proposedForDeletion: null })
		this.props.actions.invalidateEndpoint('programs')
		setSuccessAlert(toDelete.name, {
			verb: 'deleted',
		})
	}

	render() {
		const {
			initialOrdering,
			location,
			orgSlug,
			paginatedTableTxn,
			searchValue,
			tableColumns,
			tableOptions,
		} = this.props

		const { proposedForDeletion } = this.state

		return (
			<Card>
				<SearchField
					extraClassName="col-lg-6"
					initialValues={{ search: searchValue}}
				/>
				<PaginatedTableContainer
					columns={tableColumns}
					initialOrdering={initialOrdering}
					location={location}
					rowComponent={RobotMonkeyButlersListRow}
					rowProps={{
						onDelete: this.handleDeleteRequest,
						orgSlug,
					}}
					tableKey="RobotMonkeyButlersListTable"
					tableOptions={tableOptions}
					transaction={paginatedTableTxn}
				/>
				{proposedForDeletion && (
					<DeleteConfirmModal
						endpoint={'programs'}
						objectId={proposedForDeletion.id}
						onCancel={this.handleCancelDelete}
						onDelete={this.handleDelete}
					>
						<div className="p-a-1">
							<p>
								This action will delete{' '}
								<strong>{proposedForDeletion.name}.</strong>{' '}
								This action cannot be undone.
							</p>
						</div>
					</DeleteConfirmModal>
				)}
			</Card>
		)
	}
}

const mapStateToProps = (_, { location, match }) => {
	const query = queryString.parse(location.search)
	const params = {
		catalogs__in: query.catalogs // NOTE: This value is not sanitized!
	}
	const paginatedTableTxn = new Transaction('programs', params)

	const orgSlug = R.path(['params', 'organizationSlug'], match)

	const searchValue = query.search
	return {
		orgSlug,
		paginatedTableTxn,
		searchValue,
	}
}

const mapDispatchToProps = (dispatch) => {
	return {
		actions: bindActionCreators(modelActions, dispatch),
	}
}

const wrappers = R.compose(
	withRouter,
	connect(mapStateToProps, mapDispatchToProps)
)

const RobotMonkeyButlersListContainer = wrappers(RobotMonkeyButlersListContainer__Unconnected)

export { RobotMonkeyButlersListContainer }
