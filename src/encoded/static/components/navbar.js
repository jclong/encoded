'use strict';
var React = require('react');
var url = require('url');
var mixins = require('./mixins');
var productionHost = require('./globals').productionHost;
var _ = require('underscore');
var Navbar = require('react-bootstrap/lib/Navbar');
var CollapsableNav = require('react-bootstrap/lib/CollapsableNav');
var Nav = require('react-bootstrap/lib/Nav');
var NavItem = require('react-bootstrap/lib/NavItem');
var DropdownButton = require('react-bootstrap/lib/DropdownButton');
var MenuItem = require('react-bootstrap/lib/MenuItem');

// Hide data from NavBarLayout
var NavBar = React.createClass({
    render: function() {
        var section = url.parse(this.props.href).pathname.split('/', 2)[1] || '';
        return <NavBarLayout
            loadingComplete={this.props.loadingComplete}
            portal={this.props.portal}
            section={section}
            session={this.props.session}
            context_actions={this.props.context_actions}
            user_actions={this.props.user_actions}
            href={this.props.href}
            />;
    }
});


var NavBarLayout = React.createClass({
    getInitialState: function() {
        return {
            testWarning: !productionHost[url.parse(this.props.href).hostname]
        };
    },

    handleClick: function(e) {
        e.preventDefault();
        e.stopPropagation();

        // Remove the warning banner because the user clicked the close icon
        this.setState({testWarning: false});

        // If collection with .sticky-header on page, jiggle scroll position
        // to force the sticky header to jump to the top of the page.
        var hdrs = document.getElementsByClassName('sticky-header');
        if (hdrs.length) {
            window.scrollBy(0,-1);
            window.scrollBy(0,1);
        }
    },

    render: function() {
        console.log('render navbar');
        var portal = this.props.portal;
        var section = this.props.section;
        var session = this.props.session;
        var user_actions = this.props.user_actions;
        var context_actions = this.props.context_actions;
        var brand = <a href="/">{portal.portal_title}</a>;
        return (
            <div id="navbar" className="navbar navbar-fixed-top navbar-inverse">
                <div className="container">
                    <Navbar brand={brand} toggleNavKey={0} bsStyle="primary" bsClass="nav" data-target="main-nav">
                        <CollapsableNav eventKey={0}>
                            <GlobalSections global_sections={portal.global_sections} section={section} />
                            <UserActions {...this.props} />
                            {context_actions ? <ContextActions {...this.props} /> : null}
                            <Search {...this.props} />
                        </CollapsableNav>
                    </Navbar>
                </div>
                {this.state.testWarning ?
                    <div className="test-warning">
                        <div className="container">
                            <p>
                                The data displayed on this page is not official and only for testing purposes.
                                <a href="#" className="test-warning-close icon icon-times-circle-o" onClick={this.handleClick}></a>
                            </p>
                        </div>
                    </div>
                : null}
            </div>
        );
    }
});


var GlobalSections = React.createClass({
    render: function() {
        var section = this.props.section;

        // Render top-level main menu
        var actions = this.props.global_sections.map(function (action) {
            var subactions;
            if (action.children) {
                return (
                    <DropdownButton eventKey={action.id} title={action.title}>
                        {action.children.map(function (action) {
                            return (
                                <MenuItem href={action.url || ''} eventKey={action.id}>
                                    {action.title}
                                </MenuItem>
                            );
                        })}
                    </DropdownButton>
                );
            } else {
                <NavItem eventKey={action.id} href={action.url || ''}>action.title</NavItem>
            }
        });
        return <Nav navbar>{actions}</Nav>;
    }
});

var ContextActions = React.createClass({
    render: function() {
        var actions = this.props.context_actions.map(function(action) {
            return (
                <MenuItem href={action.href} eventKey={action.name}>
                    <i className="icon icon-pencil"></i> {action.title}
                </MenuItem>
            );
        });
        if (this.props.context_actions.length > 1) {
            var contextTitle = <i className="icon icon-gear"></i>;
            actions = (
                <DropdownButton title={contextTitle} eventKey="context">
                    {actions}
                </DropdownButton>
            );
        }
        return <Nav navbar right id="edit-actions">{actions}</Nav>;
    }
});

var Search = React.createClass({
    render: function() {
        var id = url.parse(this.props.href, true);
        var searchTerm = id.query['searchTerm'] || '';
        return (
            <form className="navbar-form navbar-right" action="/search/">
                <div className="search-wrapper">
                    <input className="form-control search-query" id="navbar-search" type="text" placeholder="Search ENCODE" 
                        ref="searchTerm" name="searchTerm" defaultValue={searchTerm} key={searchTerm} />
                </div>
            </form>
        );  
    }
});


var UserActions = React.createClass({
    render: function() {
        var session = this.props.session;
        var disabled = !this.props.loadingComplete;
        if (!(session && session['auth.userid'])) {
            return (
                <Nav navbar right id="user-actions">
                    <NavItem data-trigger="login" disabled={disabled}>Sign in</NavItem>
                </Nav>
            );
        }
        var actions = this.props.user_actions.map(function (action) {
            return (
                <MenuItem href={action.url || ''} eventKey={action.id} data-bypass={action.bypass} data-trigger={action.trigger}>
                    {action.title}
                </MenuItem>
            );
        });
        var fullname = (session.user_properties && session.user_properties.title) || 'unknown';
        return (
            <Nav navbar right id="user-actions">
                <DropdownButton title={fullname} eventKey="user">
                    {actions}
                </DropdownButton>
            </Nav>
        );
    }
});

module.exports = NavBar;
