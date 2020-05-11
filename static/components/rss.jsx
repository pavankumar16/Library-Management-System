import React from 'react';
class FetchDataFromRSSFeed extends React.Component {
    constructor() {
      super();
      this.state = {
        recentBlogPost: {
          name: '',
          url: ''
        },
        recentBlogPost2: {
            name: '',
            url: ''
          }
          ,
          recentBlogPost3: {
            name: '',
            url: '',
            thumbnail:''
          },
          recentBlogPost4: {
            name: '',
            url: '',
            thumbnail:''
          },
          recentBlogPost5: {
            name: '',
            url: ''
 
          }
      }
    }
  
    FetchDataFromRssFeed() {
      var request = new XMLHttpRequest();
      request.onreadystatechange = () => {
        if (request.readyState == 4 && request.status == 200) {
          var myObj = JSON.parse(request.responseText);
          //for (var i = 0; i < 10; i ++) {
            this.setState({
              recentBlogPost: {
                name: myObj.items[0].title,
                url: myObj.items[0].link
              }
            });
            this.setState({
                recentBlogPost2: {
                  name: myObj.items[1].title,
                  url: myObj.items[1].link
                }
              });
              this.setState({
                recentBlogPost3: {
                  name: myObj.items[2].title,
                  url: myObj.items[2].link,
                  thumbnail: myObj.items[2].thumbnail
                }
              });
              this.setState({
                recentBlogPost4: {
                  name: myObj.items[3].title,
                  url: myObj.items[3].link,
                  thumbnail: myObj.items[3].thumbnail
                }
              });
              this.setState({
                recentBlogPost5: {
                  name: myObj.items[4].title,
                  url: myObj.items[4].link,
                }
              });
          //}
        }
      }
      request.open("GET", "https://api.rss2json.com/v1/api.json?rss_url=http%3A%2F%2Ffetchrss.com%2Frss%2F5e98214b8a93f8231f8b45675e9821378a93f8a81e8b4567.xml", true);
      request.send();
    }
  
    componentDidMount() {
      {this.FetchDataFromRssFeed()}
    }
  
    render() {
      return (
        <div>
          <h3>Latest Tweet on #Books:</h3> <br></br><a target="_blank" href={this.state.recentBlogPost.url}>{this.state.recentBlogPost.name}</a>
          <br></br>
          <br></br>
          <a target="_blank" href={this.state.recentBlogPost2.url}>{this.state.recentBlogPost2.name}</a>
          <br></br>
          <br></br>
          <img src={this.state.recentBlogPost3.thumbnail} width="150px" height="150px"/>
          <br></br>
          <a target="_blank" href={this.state.recentBlogPost3.url}>{this.state.recentBlogPost3.name}</a>
          <br></br>
          <br></br>
          <img src={this.state.recentBlogPost4.thumbnail} width="150px" height="150px"/>
          <br></br>
          <a target="_blank" href={this.state.recentBlogPost4.url}>{this.state.recentBlogPost4.name}</a>
          <br></br>
          <br></br>
          <a target="_blank" href={this.state.recentBlogPost5.url}>{this.state.recentBlogPost5.name}</a>
        </div>

      );
    }
    
  }

  
export const RSSContainer = (FetchDataFromRSSFeed);