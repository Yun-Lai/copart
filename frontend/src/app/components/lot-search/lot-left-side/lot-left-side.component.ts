import {Component, EventEmitter, Input, OnInit, Output, OnChanges} from '@angular/core';
import { HostListener } from "@angular/core";
import {SearchService} from "../../../utils/services/search.service";
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-lot-left-side',
  templateUrl: './lot-left-side.component.html',
  styleUrls: ['./lot-left-side.component.scss']
})
export class LotLeftSideComponent implements OnInit {

  params: any;
  lots = [];
  total_lots = 0;
  pages = [];
  current_page = '1';
  current_entry = 20;
  page_start_index = 1;
  page_end_index = 20;
  filter_word = '';
  copart_count = 0;
  iaai_count = 0;
  sold_count = 0;
  features = [];
  makes = [];
  models = [];
  years = [];
  engine_types = [];
  transmissions = [];
  drive_trains = [];
  fuels = [];
  body_styles = [];
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
  status = [];

  showItems = true;

  searchFeature = "";
  searchMake = "";
  searchModel = "";
  searchYear="";
  searchBodyStyle="";
  searchFuelType="";
  searchEngineType="";
  searchTransmission="";
  searchDriveTrain="";
  page = "1";
  entry = "20";
  config = {};
  sort = '';

  apply_sold = false;

  @HostListener('window:resize', ['$event'])
  getScreenSize(event?) {

    if (window.innerWidth > 992) {
      this.showItems = true;
    } else {
      this.showItems = false
    }
  }

  constructor(private api: SearchService, private route: ActivatedRoute, private router: Router) {
    this.route.queryParams.subscribe( queryParams => {
        let params = this.route.snapshot.queryParams;
        let status = this.status;
        const paramsKeys = Object.keys(params);
        this.params = {};
        for (let key of paramsKeys) {
          this.params[key] = params[key]
        }
        if (this.params['page']) {
          this.page = this.params['page'];
          delete this.params['page']
        }
        if (this.params['entry']) {
          this.entry = this.params['entry'];
          delete this.params['entry']
        }
        if (this.params['sort']) {
          this.sort = this.params['sort'];
          delete this.params['sort']
        }
        if (this.params['status']) {
          this.status = JSON.parse(this.params['status']);
          delete this.params['status'];
        }
        if (this.applied_sold === "yes") {
          this.apply_sold = true;
        } else {
          this.apply_sold = false;
        }
        this.getListData();
      });
  }

  ngOnInit() {
    if (window.innerWidth > 992) {
      this.showItems = true;
    } else {
      this.showItems = false
    }
  }
  ngOnChanges(changes: any) {

  }

  getListData() {
    if (this.params['params']) {
      let filter_params = JSON.parse(this.params['params']);
      if (filter_params['odometers']) {
        delete filter_params['odometers']
      }
      if (filter_params['locations']) {
        delete filter_params['locations']
      }
      if (filter_params['sale_dates']) {
        delete filter_params['sale_dates']
      }
      if (filter_params['cylinderss']) {
        delete filter_params['cylinderss']
      }
      if (filter_params['vehicle_types']) {
        delete filter_params['vehicle_types']
      }
      if (filter_params['damages']) {
        delete filter_params['damages']
      }
      if (filter_params['doctypes']) {
        delete filter_params['doctypes']
      }
      this.params['params'] = JSON.stringify(filter_params)
    }

    this.api.getSearchListCount(this.params).then( result => {
      this.config = result.config;
      this.copart_count = result.copart_count;
      this.iaai_count = result.iaai_count;
      this.sold_count = result.sold_count;
    });

    this.api.getSearchListFeatures(this.params).then( result => {
      this.features = result.features;
      this.makes = result.makes;
      this.models = result.models;
    }).catch(error => {
      console.log(error);
    });

    this.api.getSearchListYearLocation(this.params).then(result => {
      this.years = result.years;
    }).catch(error => {
      console.log(error);
    });
    this.api.getSearchListFuelEngine(this.params).then(result => {
      this.fuels = result.fuels;
      this.engine_types = result.engine_types;
      this.body_styles = result.body_styles;
    }).catch(error => {
      console.log(error);
    });
    this.api.getSearchListTransmissionCylinder(this.params).then(result => {
      this.transmissions = result.transmissions;
      this.drive_trains = result.drive_trains;
    }).catch(error => {
      console.log(error);
    });
  }

  onClickItem(event) {
    let item = event.target.attributes.name.value;
    if (this.status.indexOf(item) >= 0) {
      this.status.splice(this.status.indexOf(item), 1);
    } else {
      this.status.push(item);
    }
    this.params['status'] = JSON.stringify(this.status);
    // if (this.page) {
      this.params['page'] = this.page;
    // }
    // if (this.entry) {
      this.params['entry'] = this.entry;
    // }
    this.params['sort'] = this.sort;
    this.router.navigate(
      ['/lots_by_search'],
      { queryParams: this.params});
  }
  toggleItems() {
    if (window.innerWidth > 992) {
      this.showItems = true;
    }
    this.showItems = !this.showItems;
  }
  addParams(key, value: string) {
    if (key === 'featured') {
      if (this.applied_filter_features.indexOf(value) >= 0){
        let filter = this.applied_filter_features.filter(item => item !== value);
        this.changeFilters.emit({"key": key, "value": filter});
      } else {
        let filter = Object.assign(this.applied_filter_features);
        filter.push(value);
        this.changeFilters.emit({"key": key, "value": filter});
      }
    } else if (key === 'makes') {
      if (this.applied_filter_makes.indexOf(value) >= 0){
        let filter = this.applied_filter_makes.filter(item => item !== value);
        this.changeFilters.emit({"key": key, "value": filter});
      } else {
        let filter = Object.assign(this.applied_filter_makes);
        filter.push(value);
        this.changeFilters.emit({"key": key, "value": filter});
      }
    } else if (key === 'years') {
      if (this.applied_filter_years.indexOf(value) >= 0){
        let filter = this.applied_filter_years.filter(item => item !== value);
        this.changeFilters.emit({"key": key, "value": filter});
      } else {
        let filter = Object.assign(this.applied_filter_years);
        filter.push(value);
        this.changeFilters.emit({"key": key, "value": filter});
      }
    }else if (key === 'models') {
      if (this.applied_filter_models.indexOf(value) >= 0){
        let filter = this.applied_filter_models.filter(item => item !== value);
        this.changeFilters.emit({"key": key, "value": filter});
      } else {
        let filter = Object.assign(this.applied_filter_models);
        filter.push(value);
        this.changeFilters.emit({"key": key, "value": filter});
      }
    } else if (key === 'body_styles') {
      if (this.applied_filter_body_styles.indexOf(value) >= 0){
        let filter = this.applied_filter_body_styles.filter(item => item !== value);
        this.changeFilters.emit({"key": key, "value": filter});
      } else {
        let filter = Object.assign(this.applied_filter_body_styles);
        filter.push(value);
        this.changeFilters.emit({"key": key, "value": filter});
      }
    } else if (key === 'fuels') {
      if (this.applied_filter_fuels.indexOf(value) >= 0){
        let filter = this.applied_filter_fuels.filter(item => item !== value);
        this.changeFilters.emit({"key": key, "value": filter});
      } else {
        let filter = Object.assign(this.applied_filter_fuels);
        filter.push(value);
        this.changeFilters.emit({"key": key, "value": filter});
      }
    } else if (key === 'engine_types') {
      if (this.applied_filter_engine_types.indexOf(value) >= 0){
        let filter = this.applied_filter_engine_types.filter(item => item !== value);
        this.changeFilters.emit({"key": key, "value": filter});
      } else {
        let filter = Object.assign(this.applied_filter_engine_types);
        filter.push(value);
        this.changeFilters.emit({"key": key, "value": filter});
      }
    } else if (key === 'transmissions') {
      if (this.applied_filter_transmissions.indexOf(value) >= 0){
        let filter = this.applied_filter_transmissions.filter(item => item !== value);
        this.changeFilters.emit({"key": key, "value": filter});
      } else {
        let filter = Object.assign(this.applied_filter_transmissions);
        filter.push(value);
        this.changeFilters.emit({"key": key, "value": filter});
      }
    } else if (key === 'drive_trains') {
      if (this.applied_filter_drive_trains.indexOf(value) >= 0){
        let filter = this.applied_filter_drive_trains.filter(item => item !== value);
        this.changeFilters.emit({"key": key, "value": filter});
      } else {
        let filter = Object.assign(this.applied_filter_drive_trains);
        filter.push(value);
        this.changeFilters.emit({"key": key, "value": filter});
      }
    } else if (key === 'source') {
      this.changeFilters.emit({'key': key, "value": value})
    } else if (key === 'sold') {
      if (this.apply_sold) {
        this.changeFilters.emit({'key': key, "value": "yes"})
      } else {
        this.changeFilters.emit({'key': key, "value": "no"})
      }
    }
  }
}
