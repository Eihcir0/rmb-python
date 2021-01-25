import React, { Component } from 'react'
import PropTypes from 'prop-types'
import RobotMonkeyButlerFormContainer from '~/RobotMonkeyButlers/containers/RobotMonkeyButlerFormContainer'


class RobotMonkeyButlerEditScene extends Component {
	static propTypes = {
		params: PropTypes.object.isRequired,
	}

	render() {
		const {
			params
		} = this.props
		const headerText = params.robotMonkeyButlerId ? 'Edit Robot Monkey Butler' : 'Add Robot Monkey Butler'

		// const isCreate = p

		return (
			<div>
				<h1>{headerText}</h1>
				<RobotMonkeyButlerFormContainer
					isCreate={!params.robotMonkeyButlerId}
					params={params}
				/>
			</div>
		)
	}
}

export default RobotMonkeyButlerEditScene
