import React, { Component, Fragment } from 'react'
import PropTypes from 'prop-types'

import { hasPermission, joinUrl, scrollToTop } from '~/helpers'

//(^_^)section:start:List Headers(^_^)
import PageHeader from '~/Shared/components/PageHeader'
import { AddButton } from '~/Shared/components/AddButton'
const HEADER_TITLE = 'Robot Monkey Butlers'
//(^_^)section:end(^_^)
import { RobotMonkeyButlersListContainer } from '~/RobotMonkeyButlers/containers/RobotMonkeyButlersListContainer'
import { RobotMonkeyButlersListFiltersContainer } from '~/RobotMonkeyButlers/containers/RobotMonkeyButlersListFiltersContainer'

const FORM_ID = 'robotmonkeybutlers-list-filters'

const hasReadPermissions = hasPermission('bulkuploads.add_bulkuploadrequest')

class RobotMonkeyButlersListScene extends Component {

	static propTypes = {
		history: PropTypes.object.isRequired,
		match: PropTypes.object.isRequired,
	}

	componentDidMount() {
		const { match, history } = this.props

		if (!hasReadPermissions) {
			history.push(joinUrl(match.params.organizationSlug, 'dashboard'))
		}

		scrollToTop()
	}

	render() {
		return (
			<Fragment>
				{/* (^_^)section:start:List Headers(^_^) */}
				<PageHeader title={HEADER_TITLE}>
					<AddButton
						orgSlug={this.props.match.params.organizationSlug}
						path={['robotmonkeybutlers', 'add']}
					/>
				</PageHeader>
				{/* (^_^)section:end(^_^) */}
				<RobotMonkeyButlersListFiltersContainer formId={FORM_ID} />
				<RobotMonkeyButlersListContainer
					location={this.props.location}
					formId={FORM_ID}
				/>
			</Fragment>
		)
	}
}

export { RobotMonkeyButlersListScene }
//Created by Robot.Monkey.Butlers MONKEY_DATE
