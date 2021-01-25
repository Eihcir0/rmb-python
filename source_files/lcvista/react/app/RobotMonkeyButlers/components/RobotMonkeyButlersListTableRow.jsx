import React, { Component } from 'react'
import { Link } from 'react-router'
import { joinUrl } from '~/helpers'

const Buttons = ({item, handlers, organizationSlug}) => {
	const buttons = []
	buttons.push(
		<Link
			className="btn btn-sm btn-secondary"
			to={joinUrl(
				organizationSlug,
				'RobotMonkeyButlers',
				item.id,
			)}
		>
			Edit
		</Link>
	)
	handlers.forEach(handler => {
		buttons.push(
			<button className="btn btn-sm btn-secondary m-l-half" onClick={handler[1].bind(null, item)}>
				{handler[0]}
			</button>
		)
	})
	return buttons
}

export default class RobotMonkeyButlersTableRow extends Component {
	render() {
		const {
			item,
		} = this.props

		return (
			<tbody>
				<tr key={item.id}>
					<td>
						{item.name}
					</td>
					<td>
						<Buttons {...this.props} />
					</td>
				</tr>
			</tbody>
		)
	}
}
//Created by Robot.Monkey.Butler MONKEY_DATE