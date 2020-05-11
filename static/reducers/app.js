import * as ActionTypes from '../actionCreators/actionTypes';
import {Map, List, fromJS} from 'immutable';

const initalState = fromJS({
 title: "The Bengaluru Library",
 page: 'searchBook'
});

function setPage(state,page){
  return state.set('page',page)
}

export default function(state = initalState, action) {
 switch (action.type) {
  case ActionTypes.SET_PAGE:
     return setPage(state,action.page);
 }
 return state;
}
