/** @jsx React.DOM */
'use strict';
var React = require('react');
var classSet = require('react/lib/cx');
var BootstrapMixin = require('./BootstrapMixin');
var utils = require('./utils');


var Navbar = React.createClass({
  mixins: [BootstrapMixin],

  propTypes: {
    fixedTop: React.PropTypes.bool,
    fixedBottom: React.PropTypes.bool,
    staticTop: React.PropTypes.bool,
    inverse: React.PropTypes.bool,
    noClasses: React.PropTypes.bool
  },

  getInitialState: function() {
    return {
      collapsed: true
    };
  },

  getDefaultProps: function () {
    return {
      bsClass: 'navbar',
      bsStyle: 'default',
      brandlink: '#',
      noClasses: false,
      target: "default-navbar"
    };
  },

  handleCollapse: function() {
    var collapsed = !this.state.collapsed;
    this.setState({collapsed: collapsed});
  },

  render: function () {
    var classes;

    if (!this.props.noClasses) {
      classes = this.getBsClassSet();

      classes['navbar-fixed-top'] = this.props.fixedTop;
      classes['navbar-fixed-bottom'] = this.props.fixedBottom;
      classes['navbar-static-top'] = this.props.staticTop;
      classes['navbar-inverse'] = this.props.inverse;
    }

    var toggleClass = classSet({
      "navbar-toggle": true,
      "collapsed": this.state.collapsed
    });
    var collapseClass = classSet({
      "navbar-collapse": true,
      "collapse": true,
      "in": !this.state.collapsed
    });

    var navBarCss = "navbar-brand" + (this.props.brandClasses ? ' ' + this.props.brandClasses : '');

    return (
      <nav className={classSet(classes)} role="navigation">
        <div className="navbar-header">
          <button type="button" className={toggleClass} data-toggle="collapse"
              data-target={'#' + this.props.target} onClick={this.handleCollapse}>
            <span className="sr-only">Toggle navigation</span>
            <span className="icon-bar"></span>
            <span className="icon-bar"></span>
            <span className="icon-bar"></span>
          </button>
          <a className={navBarCss} href={this.props.brandlink}><span className={this.props.hiddenBrand ? 'sr-only' : ''}>{this.props.brand}</span></a>
        </div>

        <div className={collapseClass} id={this.props.target}>
          {this.props.children}
        </div>
      </nav>
    );
  }
});

module.exports = Navbar;