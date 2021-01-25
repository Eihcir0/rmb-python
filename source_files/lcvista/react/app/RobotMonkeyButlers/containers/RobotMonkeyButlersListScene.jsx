import React, { Component } from 'react'

import RobotMonkeyButlersListFiltersContainer from '~/RobotMonkeyButlers/containers/RobotMonkeyButlersListFiltersContainer'
import RobotMonkeyButlersListContainer from '~/RobotMonkeyButlers/containers/RobotMonkeyButlersListContainer'
//(^_^)section:start:List Headers(^_^)
import Header from '~/RobotMonkeyButlers/components/RobotMonkeyButlersListHeader'

const HEADER_TITLE = 'Robot Monkey Butlers'
//(^_^)section:end(^_^)


class RobotMonkeyButlersListScene extends Component {

	componentDidMount() {
		window.scrollTo(0,0)
	}

	handleAddNew = () => {
		this.props.router.push(`${this.props.location.pathname}add/`)
	}

	render() {

		return (
			<div>
				{/* (^_^)section:start:List Headers(^_^) */}
				<Header onAddNew={this.handleAddNew} title={HEADER_TITLE} />
				{/* (^_^)section:end(^_^) */}
				<RobotMonkeyButlersListFiltersContainer/>
				<RobotMonkeyButlersListContainer/>
			</div>
		)
	}
}

export default RobotMonkeyButlersListScene
//Created by Robot.Monkey.Butlers MONKEY_DATE
