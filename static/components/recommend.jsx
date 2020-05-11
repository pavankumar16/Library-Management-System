import React from 'react';
import { connect } from 'react-redux';
import { setLoanSearchResult } from '../actionCreators/checkin'

class CheckIn extends React.Component {
 constructor(props){
   super(props);
   this.state = {loanId:[],checkin:false,success:null,message:'',searchQuery:'',isLoading:false};
   this.handleSearch = this.handleSearch.bind(this);
   this.handleCheckin = this.handleCheckin.bind(this);
   this.handleLoanSelectionChange = this.handleLoanSelectionChange.bind(this);
 }

 componentWillUnmount(){
   this.props.setLoanSearchResult(null)
 }


 handleSearch(event){
   this.setState({loanId:[],checkin:false,success:null,message:''});

   let bool = event.target.name == 'search' ? this.searchInput.value.length > 0 && event.which == 13 : this.searchInput.value.length > 0
   if(bool){
     this.props.setLoanSearchResult(null)
     this.setState({isLoading:true})
     this.setState({'searchQuery':this.searchInput.value})
     let searchJson = {'searchQuery': this.searchInput.value};
     $.ajax({
              url: 'http://localhost:5000/searchHistory',
              type: 'POST',
              data: JSON.stringify(searchJson),
              success: function(response) {
                  this.props.setLoanSearchResult(response)
                  this.setState({isLoading:false})
              }.bind(this),
              error: function(error) {
                this.setState({isLoading:false})
              }.bind(this)
          });
   }
   else{
     this.props.setLoanSearchResult(null)
   }
 }

 refreshLoanSearch(searchQuery){
   this.setState({isLoading:true})
   let searchJson = {'searchQuery': searchQuery};
   $.ajax({
            url: 'http://localhost:5000/searchHistory',
            type: 'POST',
            data: JSON.stringify(searchJson),
            success: function(response) {
                this.props.setLoanSearchResult(response)
                this.setState({isLoading:false})
            }.bind(this),
            error: function(error) {
              this.setState({isLoading:false})
            }.bind(this)
        });
 }

 handleCheckin(event){
  let bool = event.target.name == 'search' ? this.searchInput.value.length > 0 && event.which == 13 : this.searchInput.value.length > 0
  if(bool){
    let searchJson = {'searchQuery': this.searchInput.value};
     $.ajax({
              url: 'http://localhost:5000/getRecommendation',
              type: 'POST',
              data: JSON.stringify(searchJson),
              success: function(response) {
                this.props.setLoanSearchResult(response)
                //this.setState({message:response.message,success:response.success})
                //this.refreshLoanSearch(this.state.searchQuery)
              }.bind(this),
              error: function(error) {
                  this.setState({message:response.message,success:response.success})
                  this.refreshLoanSearch(this.state.searchQuery)
              }.bind(this)
          });
   }
   else{
     alert('No record selected')
   }
 }

 handleLoanSelectionChange(event){
   let newList = this.state.loanId
   if(this.state.loanId.includes(event.target.value.toString())){
     newList.pop(event.target.value)
   }
   else{
     newList.push(event.target.value)
   }
   this.setState({loanId: newList})
 }

 render(){
   let bookSearchClassName = this.props.searchLoanResult ? 'afterResult' : 'bookSearchBox'
   return <div className='checkIn'>
    <div className = 'container-fluid'>
     <div className ='row-fluid'>
      <div className ='col-md-6'>
    <div className={"input-group "+bookSearchClassName}>
     <input type="text" className="form-control" placeholder="Enter Library ID or name to get started.." name='search' onKeyPress={this.handleSearch} ref={(input)=>{this.searchInput=input}} / >
       <span className="input-group-btn">
         <button className="btn btn-primary" type="button" name = 'go' onClick={this.handleSearch}>Get History</button>
       </span>
    </div>
    </div>
    </div>
    <div className ='row-fluid'>
      <div className = 'col-md-12'>
    {
      this.props.searchLoanResult ? this.props.searchLoanResult.get('searchResult').size > 0 ? <div className='isbnTable'><table className="table defaultTable">
        <thead>
          <tr>
            <th scope="col">ISBN</th>
            <th scope="col">Title</th>
            <th scope="col">Genre</th>
            <th scope="col">Rating</th>
          </tr>
        </thead>
        <tbody>
      {
        this.props.searchLoanResult.get('searchResult').map((data,id) => {
                let loanId = data.get(0)
                return <tr key={loanId}>
                  <td>{data.get(0)}</td>
                  <td>{data.get(1)}</td>
                  <td>{data.get(2)}</td>
                  <td>{data.get(3)}</td>
                </tr>
        })
      }
    </tbody>
    </table>

    {
      this.state.success == true ?  <div className="alertSuccess">  <strong>Success!</strong> {this.state.message}  </div>
    : this.state.success == false ? <div className="alertDanger">
        <strong>Failed!</strong> {this.state.message}
      </div>
      : null
    }

  <div className = 'checkOutButton'><button type = 'button' className = 'btn btn-primary' onClick={this.handleCheckin}>Get New Recommendation</button></div>

    </div>
       :<div className='noResults'><span>No results found</span></div> : this.state.isLoading == true ? <div className = 'loadingSearch'><span>Loading...</span></div> : null
    }
   </div>
 </div>
</div>
</div>
 }
}

CheckIn.propTypes = {
  setLoanSearchResult: React.PropTypes.func,
  searchLoanResult: React.PropTypes.object
}

const mapStateToProps = (state) => {
 return {
   searchLoanResult: state.getIn(['checkin','searchLoanResult'])
 };
}

const mapDispatchToProps = (dispatch) => {
 return {
   setLoanSearchResult: (searchLoanResult) => {
     dispatch(setLoanSearchResult(searchLoanResult));
   }
 };
}

export const RecContainer = connect(mapStateToProps,
 mapDispatchToProps)(CheckIn);
