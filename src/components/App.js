import React from 'react';
import { Link }  from 'react-router';
import packageJSON from '../../package.json';

export default React.createClass({
  render() {
    const version = packageJSON.version;

    return (
      <div>
        <header>
          <h1>Circle {version}</h1>
          <Link to="/poweredby">Powered by</Link>
        </header>
        <section>
          {this.props.children || 'information and knowledge is good'}
        </section>
      </div>
    )
  }
});
