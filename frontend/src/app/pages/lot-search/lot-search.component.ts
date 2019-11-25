import { Component, OnInit } from '@angular/core';
import {SearchService} from "../../utils/services/search.service";
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-lot-search',
  templateUrl: './lot-search.component.html',
  styleUrls: ['./lot-search.component.scss']
})
export class LotSearchComponent implements OnInit {

  params = {};

  applied_filter_source = '';
  applied_sold = "no";
  applied_filter_features = [];
  applied_filter_makes = [];
  applied_filter_models = [];
  applied_filter_years = [];
  applied_filter_engine_types = [];
  applied_filter_transmissions = [];
  applied_filter_drive_trains = [];
  applied_filter_fuels = [];
  applied_filter_body_styles = [];
  updateFilters = false;

  constructor(private api: SearchService, private route: ActivatedRoute, private router: Router) {
    this.params = this.route.snapshot.queryParams;
  }

  ngOnInit() {
    if (this.params['params'])
    {
      let params = JSON.parse(this.params['params']);
      let keys = ['source', 'sold', 'featured', 'makes', 'models', 'years', 'engine_types', 'transmissions', 'drive_trains',
        'fuels', 'body_styles'];
      for (let key of keys) {
        if (params[key] && params[key].length > 0) {
          if (key === 'featured') {
            this.applied_filter_features = params[key]
          } else if (key === 'makes') {
            this.applied_filter_makes = params[key]
          } else if (key === 'makes') {
            this.applied_filter_models = params[key]
          } else if (key === 'models') {
            this.applied_filter_makes = params[key]
          } else if (key === 'years') {
            this.applied_filter_years = params[key]
          } else if (key === 'engine_types') {
            this.applied_filter_engine_types = params[key]
          } else if (key === 'transmissions') {
            this.applied_filter_transmissions = params[key]
          } else if (key === 'drive_trains') {
            this.applied_filter_drive_trains = params[key]
          } else if (key === 'fuels') {
            this.applied_filter_fuels = params[key]
          } else if (key === 'body_styles') {
            this.applied_filter_body_styles = params[key]
          } else if (key === 'sold') {
            this.applied_sold = params['key']
          }
        }
      }
      this.updateFilters = !this.updateFilters;
    }
  }
  onChangeFilters(event) {
    if (event.key === 'featured') {
      this.applied_filter_features = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'makes') {
      this.applied_filter_makes = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'models') {
      this.applied_filter_models = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'years') {
      this.applied_filter_years = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'body_styles') {
      this.applied_filter_body_styles = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'fuels') {
      this.applied_filter_fuels = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'engine_types') {
      this.applied_filter_engine_types = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'transmissions') {
      this.applied_filter_transmissions = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'drive_trains') {
      this.applied_filter_drive_trains = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'source') {
      this.applied_filter_source = event.value;
    } else if (event.key === 'sold') {
      this.applied_sold = event.value;
    }
    let params = {
      'source': this.applied_filter_source,
      'sold': this.applied_sold,
      'featured': this.applied_filter_features,
      'makes': this.applied_filter_makes,
      'models': this.applied_filter_models,
      'years': this.applied_filter_years,
      'engine_types': this.applied_filter_engine_types,
      'transmissions': this.applied_filter_transmissions,
      'drive_trains': this.applied_filter_drive_trains,
      'fuels': this.applied_filter_fuels,
      'body_styles': this.applied_filter_body_styles,
    };
    let keys = ['source', 'featured', 'makes', 'models', 'years', 'engine_types', 'transmissions', 'drive_trains',
      'fuels', 'body_styles'];
    for (let key of keys) {
      if ((params[key]).length === 0) {
        delete params[key];
      }
    }
    if (params['sold'] === "no") {
      delete params['sold'];
    }
    this.params = this.route.snapshot.queryParams;
    const paramsKeys = Object.keys(this.params);
    let queryParam = {};
    for (let key in paramsKeys) {
      queryParam[key] = this.params[key]
    }
    if (queryParam['params'])
    {
      queryParam['params'] = JSON.stringify(params);
    } else {
      queryParam = {...this.params, ...{"params": JSON.stringify(params)}}
    }
    this.router.navigate(
      [],
      { queryParams: queryParam, replaceUrl: true });
    this.updateFilters = !this.updateFilters;
  }


}
