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
  applied_filter_odometers = [];
  applied_filter_locations = [];
  applied_filter_sale_dates = [];
  applied_filter_engine_types = [];
  applied_filter_transmissions = [];
  applied_filter_drive_trains = [];
  applied_filter_cylinders = [];
  applied_filter_fuels = [];
  applied_filter_body_styles = [];
  applied_filter_vehicle_types = [];
  applied_filter_damages = [];
  applied_filter_doctypes = [];
  updateFilters = false;

  constructor(private api: SearchService, private route: ActivatedRoute, private router: Router) {
    this.params = this.route.snapshot.queryParams;
  }

  ngOnInit() {
    if (this.params['params'])
    {
      let params = JSON.parse(this.params['params']);
      let keys = ['source', 'sold', 'featured', 'makes', 'models', 'years', 'odometers', 'locations', 'sale_dates', 'engine_types', 'transmissions', 'drive_trains',
        'cylinderss', 'fuels', 'body_styles', 'vehicle_types', 'damages', 'doctypes'];
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
          } else if (key === 'odometers') {
            this.applied_filter_odometers = params[key]
          } else if (key === 'locations') {
            this.applied_filter_locations = params[key]
          } else if (key === 'sale_dates') {
            this.applied_filter_sale_dates = params[key]
          } else if (key === 'engine_types') {
            this.applied_filter_engine_types = params[key]
          } else if (key === 'transmissions') {
            this.applied_filter_transmissions = params[key]
          } else if (key === 'drive_trains') {
            this.applied_filter_drive_trains = params[key]
          } else if (key === 'cylinderss') {
            this.applied_filter_cylinders = params[key]
          } else if (key === 'fuels') {
            this.applied_filter_fuels = params[key]
          } else if (key === 'body_styles') {
            this.applied_filter_body_styles = params[key]
          } else if (key === 'vehicle_types') {
            this.applied_filter_vehicle_types = params[key]
          } else if (key === 'damages') {
            this.applied_filter_damages = params[key]
          } else if (key === 'doctypes') {
            this.applied_filter_doctypes = params[key]
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
    } else if (event.key === 'odometers'){
      this.applied_filter_odometers = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'locations') {
      this.applied_filter_locations = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'sale_dates') {
      this.applied_filter_sale_dates = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'doctypes') {
      this.applied_filter_doctypes = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'vehicle_types') {
      this.applied_filter_vehicle_types = event.value;
      // this.updateFilters = !this.updateFilters;
    } else if (event.key === 'damages') {
      this.applied_filter_damages = event.value;
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
    } else if (event.key === 'cylinderss') {
      this.applied_filter_cylinders = event.value;
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
      'odometers': this.applied_filter_odometers,
      'locations': this.applied_filter_locations,
      'sale_dates': this.applied_filter_sale_dates,
      'engine_types': this.applied_filter_engine_types,
      'transmissions': this.applied_filter_transmissions,
      'drive_trains': this.applied_filter_drive_trains,
      'cylinderss': this.applied_filter_cylinders,
      'fuels': this.applied_filter_fuels,
      'body_styles': this.applied_filter_body_styles,
      'vehicle_types': this.applied_filter_vehicle_types,
      'damages': this.applied_filter_damages,
      'doctypes': this.applied_filter_doctypes
    };
    let keys = ['source', 'featured', 'makes', 'models', 'years', 'odometers', 'locations', 'sale_dates', 'engine_types', 'transmissions', 'drive_trains',
      'cylinderss', 'fuels', 'body_styles', 'vehicle_types', 'damages', 'doctypes'];
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
