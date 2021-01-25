import React from 'react'

export default function Header({ title, onAddNew }) {
    let button = null
    if (onAddNew) {
        button = (
            <button className="btn btn-sm btn-primary m-l-1" onClick={onAddNew}>
                Add
            </button>
        )
    }
    return (
        <h1>
            {title}
            {button}
        </h1>
    )

}
//Created by Robot.Monkey.Butler MONKEY_DATE
