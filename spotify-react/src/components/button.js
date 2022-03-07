import React from 'react';

function Button({label}){
    return (<div data-testid="button" className={"button-style"}>{label}</div>)
}

export default Button;