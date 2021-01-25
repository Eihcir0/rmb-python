import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { joinUrl } from '~/helpers'
import RowActionDropdown, { DropdownItem } from '~/Shared/containers/ActionRowDropdown';

const RobotMonkeyButlersListRow = ({ item, onDelete, orgSlug }) => {
	return (
		<tr key={item.id}>
			<td>
				{item.id}
			</td>
			<td>
				<RowActionDropdown onDelete={onDelete.bind(null, item)}>
					<DropdownItem
						icon="pen"
						to={joinUrl(orgSlug, 'robotmonkeybutlers', item.id)}
					>
						Edit
					</DropdownItem>

				</RowActionDropdown>
			</td>
		</tr>
	)
}

RobotMonkeyButlersListRow.propTypes = {
	item: PropTypes.object
}

export { RobotMonkeyButlersListRow }