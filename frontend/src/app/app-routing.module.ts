import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import {StartComponent} from "./pages/start/start.component";
import {LotBySearchComponent} from "./pages/lot-by-search/lot-by-search.component";
import {DetailComponent} from "./pages/detail/detail.component";


const routes: Routes = [
  {
    path: '',
    component: StartComponent
  },
  {
    path: 'lots_by_search',
    component: LotBySearchComponent
  },
  {
    path: 'lot/:lot',
    component: DetailComponent,
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
