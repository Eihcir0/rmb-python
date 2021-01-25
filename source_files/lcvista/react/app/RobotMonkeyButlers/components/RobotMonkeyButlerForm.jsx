import React from 'react'
import { Field, reduxForm } from 'redux-form'

import FormGroup from '~/Forms/components/FormGroup'
import SubmitButton from '~/Forms/components/SubmitButton'

function RobotMonkeyButlerForm({
	error,
	handleSubmit,
	pristine,
	submitting,
	submitSucceeded,
}) {
	return (
		<form onSubmit={handleSubmit}>
			<div>
				<div className="form-group row">
					<div className="col-lg-12">
						<Field
							className="form-control"
							component={FormGroup}
							inputComponent="input"
							label="Name"
							name="name"
							required
						/>
					</div>
				</div>
			</div>
			{error && (
				<div className="text-danger m-b-1">{error.map(e => <div>{e}</div>)}</div>
			)}
			<div className="col-lg-6">
				<SubmitButton
					pristine={pristine}
					submitSucceeded={submitSucceeded}
					submitting={submitting}
				/>
			</div>
		</form>
		)
}

export default reduxForm({
	form: 'RobotMonkeyButlerForm',
	enableReinitialize: true,
})(RobotMonkeyButlerForm)
