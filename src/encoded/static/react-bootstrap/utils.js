'use strict';
var cloneWithProps = require('react/lib/cloneWithProps');

// From https://www.npmjs.org/package/extend
var hasOwn = Object.prototype.hasOwnProperty;
var toString = Object.prototype.toString;

function isPlainObject(obj) {
  if (!obj || toString.call(obj) !== '[object Object]' || obj.nodeType || obj.setInterval)
    return false;

  var has_own_constructor = hasOwn.call(obj, 'constructor');
  var has_is_property_of_method = hasOwn.call(obj.constructor.prototype, 'isPrototypeOf');
  // Not own constructor property must be Object
  if (obj.constructor && !has_own_constructor && !has_is_property_of_method)
    return false;

  // Own properties are enumerated firstly, so to speed up,
  // if last one is own, then all properties are own.
  var key;
  for ( key in obj ) {}

  return key === undefined || hasOwn.call( obj, key );
}

module.exports = {

  /**
   * Modify each item in a React children array without
   * unnecessarily allocating a new array.
   *
   * @param {array|object} children
   * @param {function} modifier
   * @returns {*}
   */
  modifyChildren: function (children, modifier) {
    if (children === null) {
      return children;
    }

    return Array.isArray(children) ? children.map(modifier) : modifier(children, 0);
  },

  /**
   * Filter each item in a React children array without
   * unnecessarily allocating a new array.
   *
   * @param {array|object} children
   * @param {function} filter
   * @returns {*}
   */
  filterChildren: function (children, filter) {
    if (children === null) {
      return children;
    }

    if (Array.isArray(children)) {
      return children.filter(filter);
    } else {
      return filter(children, 0) ? children : null;
    }
  },


  /**
   * Safe chained function
   *
   * Will only create a new function if needed,
   * otherwise will pass back existing functions or null.
   *
   * @param {function} one
   * @param {function} two
   * @returns {function|null}
   */
  createChainedFunction: function (one, two) {
    var hasOne = typeof one === 'function';
    var hasTwo = typeof two === 'function';

    if (!hasOne && !hasTwo) { return null; }
    if (!hasOne) { return two; }
    if (!hasTwo) { return one; }

    return function chainedFunction() {
      one.apply(this, arguments);
      two.apply(this, arguments);
    };
  },

  /**
   * Sometimes you want to change the props of a child passed to you. Usually
   * this is to add a CSS class.
   *
   * @param {object} child child component you'd like to clone
   * @param {object} props props you'd like to modify. They will be merged
   * as if you used `transferPropsTo()`.
   * @return {object} a clone of child with props merged in.
   */
  cloneWithProps: function (child, props) {
    return cloneWithProps(child, props);
  },
};