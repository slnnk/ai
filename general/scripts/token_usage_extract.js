// Static AST inspection only. Transcript JavaScript is never evaluated.
'use strict';
const acorn = require('acorn');
const fs = require('fs');
function extract(source) {
  const result = {calls: [], unresolved: 0, parse_error: 0, exec_nodes: 0, unavailable: 0};
  let ast;
  try {
    ast = acorn.parse(source, {ecmaVersion: 'latest', sourceType: 'module', allowAwaitOutsideFunction: true});
  } catch (_) { result.parse_error = 1; return result; }
  function value(node, env) {
    if (!node) return undefined;
    if (node.type === 'Literal') return node.value;
    if (node.type === 'Identifier') return env.get(node.name);
    if (node.type === 'TemplateLiteral') {
      let text = node.quasis[0].value.cooked;
      for (let i = 0; i < node.expressions.length; i++) {
        const part = value(node.expressions[i], env);
        if (part === undefined) return undefined;
        text += part + node.quasis[i + 1].value.cooked;
      }
      return text;
    }
    if (node.type === 'BinaryExpression' && node.operator === '+') {
      const left = value(node.left, env), right = value(node.right, env);
      if (left !== undefined && right !== undefined) return left + right;
    }
    if (node.type === 'ObjectExpression') {
      const object = Object.create(null);
      for (const property of node.properties) {
        if (property.type === 'SpreadElement') {
          const spread = value(property.argument, env);
          if (!spread || typeof spread !== 'object') return undefined;
          Object.assign(object, spread);
        } else {
          const key = property.computed ? value(property.key, env) : property.key.name ?? property.key.value;
          if (key === undefined || property.kind !== 'init' || property.method) return undefined;
          object[key] = value(property.value, env);
        }
      }
      return object;
    }
    if (node.type === 'ArrayExpression') return node.elements.map(item => value(item, env));
    if (node.type === 'MemberExpression') {
      const object = value(node.object, env);
      const key = node.computed ? value(node.property, env) : node.property.name;
      if (object && Object.prototype.hasOwnProperty.call(object, key)) return object[key];
    }
    return undefined;
  }
  function walk(node, env) {
    if (!node || typeof node !== 'object') return;
    if (node.type === 'BlockStatement' || /Function/.test(node.type)) {
      env = new Map(env);
      for (const param of node.params || []) if (param.type === 'Identifier') env.delete(param.name);
    }
    if (node.type === 'VariableDeclarator' && node.id.type === 'Identifier') {
      env.set(node.id.name, value(node.init, env));
    }
    if (node.type === 'AssignmentExpression' && node.left.type === 'Identifier') env.delete(node.left.name);
    if (node.type === 'UpdateExpression' && node.argument.type === 'Identifier') env.delete(node.argument.name);
    if (node.type === 'CallExpression') {
      const callee = node.callee;
      const name = callee.type === 'MemberExpression' ?
        (callee.computed ? value(callee.property, env) : callee.property.name) : callee.name;
      if (name === 'exec_command') {
        result.exec_nodes++;
        const argument = value(node.arguments[0], env);
        if (argument && typeof argument.cmd === 'string' &&
            (!Object.prototype.hasOwnProperty.call(argument, 'workdir') ||
             argument.workdir === null || typeof argument.workdir === 'string')) {
          const call = {cmd: argument.cmd};
          if (typeof argument.workdir === 'string') call.workdir = argument.workdir;
          result.calls.push(call);
        } else result.unresolved++;
      }
    }
    for (const [key, child] of Object.entries(node)) {
      if (key === 'start' || key === 'end') continue;
      if (Array.isArray(child)) for (const item of child) walk(item, env);
      else if (child && typeof child === 'object') walk(child, env);
    }
  }
  walk(ast, new Map());
  return result;
}
process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0, 'utf8')).map(extract)));
