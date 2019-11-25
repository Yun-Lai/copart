import {
  Component,
  OnInit,
  ViewEncapsulation,
  Input,
  HostListener,
  OnChanges,
  Output,
  EventEmitter
} from '@angular/core';
import {DataShareService} from "../../../utils/services/data-share.service";
import {ActivatedRoute} from "@angular/router";
import {SearchService} from "../../../utils/services/search.service";
import { Title } from '@angular/platform-browser';
import {LoaderService} from "../../../utils/services/loader.service";
import {ModelService} from "../../../utils/services/model.service";
import {Router} from "@angular/router";


@Component({
  selector: 'app-lot-search-list',
  templateUrl: './lot-search-list.component.html',
  styleUrls: [
    './lot-search-list.component.scss'
  ],
  encapsulation: ViewEncapsulation.None,
})
export class LotSearchListComponent implements OnInit {

  filter_word = '';
  @Input() applied_filter_source: any;
  @Input() applied_sold: any;
  @Input() applied_filter_features = [];
  @Input() applied_filter_makes = [];
  @Input() applied_filter_models = [];
  @Input() applied_filter_years = [];
  @Input() applied_filter_engine_types = [];
  @Input() applied_filter_transmissions = [];
  @Input() applied_filter_drive_trains = [];
  @Input() applied_filter_fuels = [];
  @Input() applied_filter_body_styles = [];
  @Input() updated;

  @Output() changeFilters = new EventEmitter();

  pages = [];
  page_start_index = 0;
  page_end_index = 0;
  total_lots =  0;
  current_entry = 20;
  current_page = '1';
  t_page: number;

  lots = [];
  params: any;
  order = {"sort_by":"year", "sort_type":"desc"};
  showColspan = 11;
  status = [];


  @HostListener('window:resize', ['$event'])
  getScreenSize(event?) {
    if ((window.innerWidth > 1156) || ( window.innerWidth < 992 && window.innerWidth > 933)){
      document.getElementById('c_seach_tb').classList.remove('collapsed')
    } else {
      document.getElementById('c_seach_tb').classList.add('collapsed')
    }
    if (window.innerWidth > 1156) {
      this.showColspan = 11;
    } else if(window.innerWidth > 1020) {
      this.showColspan = 10;
    } else if (window.innerWidth > 991) {
      this.showColspan = 9;
    } else if (window.innerWidth > 933) {
      this.showColspan = 11
    } else if (window.innerWidth > 797) {
      this.showColspan = 10
    } else if (window.innerWidth > 740) {
      this.showColspan = 9
    } else if (window.innerWidth > 631) {
      this.showColspan = 8;
    } else if (window.innerWidth > 596) {
      this.showColspan = 7
    } else if (window.innerWidth > 531) {
      this.showColspan = 6
    } else if (window.innerWidth > 487) {
      this.showColspan = 5
    } else if (window.innerWidth > 398) {
      this.showColspan = 4
    } else if (window.innerWidth > 312) {
      this.showColspan = 3
    } else if (window.innerWidth > 222) {
      this.showColspan = 2
    } else {
      this.showColspan = 1
    }
  }

  constructor(public dataShare: DataShareService, private route: ActivatedRoute, private router: Router,
              private api: SearchService, private title: Title, private _loader: LoaderService) {
    // this.dataShare.currentFilterWord.subscribe( res => {
    //   this.filter_word = res;
    // });

    // this.params = this.route.snapshot.queryParams;

    this.route.queryParams.subscribe( queryParams => {
      let params = this.route.snapshot.queryParams;
      let status = this.status;
      const paramsKeys = Object.keys(params);
      this.params = {};
      for (let key of paramsKeys) {
        this.params[key] = params[key]
      }
      if (paramsKeys.indexOf('page') < 0) {
        this.params['page'] = 1
      }
      if (paramsKeys.indexOf('entry') < 0) {
        this.params['entry'] = 20
      }
      if (this.params['status']) {
        this.status = this.params['status'];
        console.log("----===========----------", this.status);
        delete this.params['status']
      }
      console.log("==================", this.status);
      if (status.length === 0 || status === this.status)
      {
        this.getData();
      }
    });
  }

  ngOnInit() {
    if (window.innerWidth > 1156) {
      this.showColspan = 11;
    } else if(window.innerWidth > 1020) {
      this.showColspan = 10;
    } else if (window.innerWidth > 991) {
      this.showColspan = 9;
    } else if (window.innerWidth > 933) {
      this.showColspan = 11
    } else if (window.innerWidth > 797) {
      this.showColspan = 10
    } else if (window.innerWidth > 740) {
      this.showColspan = 9
    } else if (window.innerWidth > 631) {
      this.showColspan = 8;
    } else if (window.innerWidth > 596) {
      this.showColspan = 7
    } else if (window.innerWidth > 531) {
      this.showColspan = 6
    } else if (window.innerWidth > 487) {
      this.showColspan = 5
    } else if (window.innerWidth > 398) {
      this.showColspan = 4
    } else if (window.innerWidth > 312) {
      this.showColspan = 3
    } else if (window.innerWidth > 222) {
      this.showColspan = 2
    } else {
      this.showColspan = 1
    }

    if (this.filter_word === '') {
      this.title.setTitle('Search')
    } else {
      this.title.setTitle(this.filter_word);
    }
    if ((window.innerWidth > 1156) || ( window.innerWidth < 992 && window.innerWidth > 933)){
      document.getElementById('c_seach_tb').classList.remove('collapsed')
    } else {
      document.getElementById('c_seach_tb').classList.add('collapsed')
    }
  }
  showHiddenItems(lot) {
    let index = this.lots.indexOf(lot)
    if (this.lots[index]['showHidden'] === true) {
      this.lots[index]['showHidden'] = false;
    } else {
      this.lots[index]['showHidden'] = true;
    }
  }
  ngOnChanges(changes: any) {
    // let params = {
    //   'source': this.applied_filter_source,
    //   'featured': this.applied_filter_features,
    //   'makes': this.applied_filter_makes,
    //   'models': this.applied_filter_models,
    //   'years': this.applied_filter_years,
    //   'odometers': this.applied_filter_odometers,
    //   'locations': this.applied_filter_locations,
    //   'sale_dates': this.applied_filter_sale_dates,
    //   'engine_types': this.applied_filter_engine_types,
    //   'transmissions': this.applied_filter_transmissions,
    //   'drive_trains': this.applied_filter_drive_trains,
    //   'cylinderss': this.applied_filter_cylinders,
    //   'fuels': this.applied_filter_fuels,
    //   'body_styles': this.applied_filter_body_styles,
    //   'vehicle_types': this.applied_filter_vehicle_types,
    //   'damages': this.applied_filter_damages,
    //   'doctypes': this.applied_filter_doctypes
    // };
    // if (this.params['params'])
    // {
    //   this.params['params'] = JSON.stringify(params);
    // } else {
    //   this.params = {...this.params, ...{"params": JSON.stringify(params)}}
    // }
    // this.params = this.route.snapshot.queryParams;
    // let params = this.route.snapshot.queryParams;
    // const paramsKeys = Object.keys(params);
    // console.log(paramsKeys);
    // this.params = {};
    // for (let key of paramsKeys) {
    //   this.params[key] = params[key]
    // }
    // if (paramsKeys.indexOf('page') < 0) {
    //   this.params['page'] = 1
    // }
    // if (paramsKeys.indexOf('entry') < 0) {
    //   this.params['entry'] = 20
    // }
    // if (this.params['status']) {
    //     delete this.params['status']
    //   }
    // // this.params = {...this.params, ...{"entry": this.current_entry, 'page': 1, "sort": JSON.stringify(this.order)}};
    // this.getSearchKey();
    // this.getData()
  }
  getSearchKey() {
    this.api.getSearchKey(this.params).then( (resp) => {
      this.filter_word = resp.filter_word
    }).catch(error => {
      console.log(error)
    })
  }

  urlEncode() {
    const paramsKeys = Object.keys(this.params);
      for (let key of paramsKeys) {
        this.params[key] = this.params[key]
      }
  }
  getData() {
    this._loader.display(true);
    if (typeof (this.params.page) === 'string' && parseInt(this.params.page) < 1) {
      this.params.page = 1;
    }
    this.getSearchKey();
    this.api.getPagnagedData(this.params).then( rep => {
      this.lots = rep.lots;
      this.pages = rep.pages;
      this.current_page = rep.current_page;
      this.current_entry = rep.current_entry;
      this.page_start_index = rep.page_start_index;
      this.page_end_index = rep.page_end_index;
      this.total_lots = rep.total_lots;
      if (parseInt(this.current_page) > parseInt(this.pages[2])) {
        this.current_page = this.pages[2]
      }
      this._loader.display(false);
      if (this.lots.length === 0) {
        this.router.navigate(['/']);
      }
    }).catch( error => {
      console.log(error);
      this._loader.display(false);
      this.router.navigate(['/']);
    })
  }

  changeEntry() {
    this.params.entry = this.current_entry;
    // this.params.page = 1;
    // this.getData();
    this.params.status = this.status;
    this.router.navigate(
      ['/lots_by_search'],
      { queryParams: this.params});
  }
  changePage(page) {
    if (page === 'First') {
      this.params.page = '1';
    } else if (page === 'Last') {
      this.params.page = parseInt(this.pages[2]);
    } else if (page === 'Next') {
      if (parseInt(this.current_page) >= parseInt(this.pages[2])) {
        return;
      }
      this.params.page = (parseInt(this.current_page)+1).toString();

    } else if (page === "Previous") {
      if ((this.params.page === '1') || (this.params.page === 1)) {
        return ;
      }
      this.params.page = (parseInt(this.current_page)-1).toString()
    } else if ( page === '...' ){
      return
    } else {
      if (page > parseInt(this.params[2])) {
        this.params.page = this.params[2]
      } else if (page < 1){
        this.params.page = 1;
      } else {
        this.params.page = page;
      }
    }
    // this.urlEncode();
    this.params.status = this.status;
    this.router.navigate(
      ['/lots_by_search'],
      { queryParams: this.params});
    // this.getData();
  }
  goToPage(){
    this.params.page = this.t_page;
    if (this.t_page > parseInt(this.pages[2])) {
      this.params.page = parseInt(this.pages[2])
    }
    // this.urlEncode();
    this.params.status = this.status;
    this.router.navigate(
      ['/lots_by_search'],
      { queryParams: this.params});
  }
  gotoTop() {
    window.scroll(0, 0);
  }
  removeFilters(key, value){
    if (key === 'featured') {
      let filter = this.applied_filter_features.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    } else if (key === 'makes') {
      let filter = this.applied_filter_makes.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    } else if (key === 'models') {
      let filter = this.applied_filter_models.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    } else if (key === 'years') {
      let filter = this.applied_filter_years.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    } else if (key === 'body_styles') {
      let filter = this.applied_filter_body_styles.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    } else if (key === 'fuels') {
      let filter = this.applied_filter_fuels.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    } else if (key === 'engine_types') {
      let filter = this.applied_filter_engine_types.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    } else if (key === 'transmissions') {
      let filter = this.applied_filter_transmissions.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    } else if (key === 'drive_trains') {
      let filter = this.applied_filter_drive_trains.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    }
  }
  reOrder(type: string) {
    if (this.order.sort_by === type) {
      if (this.order.sort_type === "desc") {
        this.order.sort_type = 'asc'
      } else {
        this.order.sort_type = 'desc'
      }
    } else {
      this.order.sort_by = type;
      this.order.sort_type = 'desc'
    }
    this.params['page'] = 1;
    this.params['sort'] = JSON.stringify(this.order);
    // this.urlEncode();
    this.params.status = this.status;
    this.router.navigate(
      ['/lots_by_search'],
      { queryParams: this.params});
    // this.getData();
  }
}
