import React, { Component, Fragment } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { withRouter } from 'react-router'
import {change, getFormValues} from 'redux-form'

import R from 'ramda'

import { setSuccessAlert } from '~/Alerts/helpers'
import * as modelActions from '~/Models/actions'
import { get } from '~/Models/helpers/query'
import Transaction, {
	// RELATED_IDS,
	objectsWithTransactionsEqual,
	fetchTransactions,
} from '~/Models/helpers/Transaction'
import Loader from '~/Shared/components/Loader'
import { joinUrl } from '~/helpers'
import { validateRequired, } from '~/helpers/forms'

const FORM_ID = 'RobotMonkeyButlerForm'
import RobotMonkeyButlerForm from '~/RobotMonkeyButlers/components/RobotMonkeyButlerForm'

export const validate = (values) => {
    const requireds = ['name']
    const errors = validateRequired(requireds, values)
    return errors
}


class RobotMonkeyButlerFormContainer extends Component {

	static propTypes = {
		params: PropTypes.object.isRequired,
		isCreate: PropTypes.bool.isRequired,
	}

	componentDidMount() {
		fetchTransactions(
			this.props.robotMonkeyButlerTxn,
		)
	}

	shouldComponentUpdate(nextProps, nextState) {
		return !(objectsWithTransactionsEqual(this.props, nextProps) && R.equals(this.state, nextState))
	}

	componentDidUpdate() {
		fetchTransactions(
			this.props.robotMonkeyButlerTxn,
		)
	}

	getInitialValues = () => {
		const {
			robotMonkeyButler
		} = this.props

		const initialValues = {}
		if (robotMonkeyButler) {
			initialValues['name'] = robotMonkeyButler['name']
		}
		return initialValues
	}

	handleSubmit = (data) => {
		const {
			isCreate,
			actions,
		} = this.props

		const {
			name,
		} = data

		const submitData = {
			name,
		}

		if (isCreate) {
			return new Promise(resolve => {
				actions.postItem(
					'robotmonkeybutlers',
					{
						...submitData,
					},
				).then(data => resolve(data))
			})
		} else {
			return new Promise(resolve => {
				actions.patchItem(
					'robotmonkeybutlers',
					this.props.robotMonkeyButler.id,
					{
						...submitData,
					},
				).then(data => resolve(data))
			})
		}
	}

	handleSubmitSuccess = (response) => {
		const {
			isCreate,
			organization,
		} = this.props
		const alertOptions = {}

		if (!isCreate) alertOptions.verb = 'updated'
		setSuccessAlert(response.data.name, alertOptions)

		const pathname = joinUrl(
			organization.slug,
			'robotmonkeybutlers',
		)

		this.props.actions.invalidateEndpoint('robotmonkeybutlers')

		this.props.router.push({
			pathname,
		})
	}


	render() {
		const {
			formValues,
			robotMonkeyButler,
			robotMonkeyButlerTxn,
		} = this.props

		if (robotMonkeyButlerTxn && (!robotMonkeyButlerTxn.allFetched() || !robotMonkeyButler)) return <Loader/>

		return (
			<Fragment>
				<RobotMonkeyButlerForm
					form={FORM_ID}
					formValues={formValues}
					initialValues={this.getInitialValues()}
					onSubmit={this.handleSubmit}
					onSubmitSuccess={this.handleSubmitSuccess}
					validate={validate}
				/>
			</Fragment>
		)
	}

}

const mapStateToProps = (state, { params }) => {
	const { robotMonkeyButlerId } = params
	const isCreate = Boolean(!robotMonkeyButlerId)
	const organization = get(state, 'organizations', { slug: params.organizationSlug })
	const robotMonkeyButlerTxn = !isCreate && new Transaction(
		'robotmonkeybutlers',
		{ id__in: robotMonkeyButlerId },
		{}, // related txns
		{}, //options
	)
	const robotMonkeyButler = robotMonkeyButlerTxn && robotMonkeyButlerTxn.allFetched() && robotMonkeyButlerTxn.toArray()[0]

	return {
		formValues: getFormValues(FORM_ID)(state),	// a dict of form values
		isCreate,
		organization,
		robotMonkeyButler,
		robotMonkeyButlerTxn,
	}
}


const mapDispatchToActions = (dispatch) => {
	return {
		actions: bindActionCreators({
			change,
			...modelActions,
		}, dispatch)
	}
}


export default connect(
	mapStateToProps,
	mapDispatchToActions,
)(withRouter(RobotMonkeyButlerFormContainer))
