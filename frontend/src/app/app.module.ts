import { BrowserModule } from '@angular/platform-browser';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {APP_INITIALIZER, NgModule} from '@angular/core';

import { AppRoutingModule } from './app-routing.module';

import { DialogModule } from '@syncfusion/ej2-angular-popups';

import { AppComponent } from './app.component';
import { StartComponent } from './pages/start/start.component';
import {SharedModule} from "./shared/shared.module";
import { HttpClient, HttpClientModule } from '@angular/common/http';
import {HostService} from "./utils/services/host.service";
import { BrowseInventoryComponent } from './components/home/browse-inventory/browse-inventory.component';
import { VehicleFinderComponent } from './components/home/vehicle-finder/vehicle-finder.component';
import { NewArrivalComponent } from './components/home/new-arrival/new-arrival.component';
import { TypeNamePipe } from './utils/pipe/type-name.pipe';
import { GetImagePipe } from './utils/pipe/get-image.pipe';
import { LotBySearchComponent } from './pages/lot-by-search/lot-by-search.component';
import { LeftSideComponent } from './components/search/left-side/left-side.component';
import { SearchListComponent } from './components/search/search-list/search-list.component';
import { IsIconPipe } from './utils/pipe/is-icon.pipe';
import {LoaderService} from "./utils/services/loader.service";
import { ModelService } from './utils/services/model.service';
import { DetailComponent } from './pages/detail/detail.component';
import { LotDetailComponent } from './components/details/lot-detail/lot-detail.component';
import { LotSimilarComponent } from './components/details/lot-similar/lot-similar.component';
import { GetHighlightPipe } from './utils/pipe/get-highlight.pipe';
import { ZoomImageComponent } from './components/details/zoom-image/zoom-image.component';
import { ModalComponent } from './components/details/lot-detail/jw-modal/jw-modal.component';
import { SafePipe } from './utils/pipe/safe.pipe';
// import * as $ from 'jquery';

export function launchAppConfig(hostService: HostService, http: HttpClient) { return () => hostService.init(http); }

@NgModule({
  imports: [
    BrowserModule,
    AppRoutingModule,
    SharedModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    DialogModule
  ],
  declarations: [
    AppComponent,
    StartComponent,
    BrowseInventoryComponent,
    VehicleFinderComponent,
    NewArrivalComponent,
    TypeNamePipe,
    GetImagePipe,
    LotBySearchComponent,
    LeftSideComponent,
    SearchListComponent,
    IsIconPipe,
    DetailComponent,
    LotDetailComponent,
    LotSimilarComponent,
    GetHighlightPipe,
    ZoomImageComponent,
    ModalComponent,
    SafePipe,
  ],
  providers: [
    { provide: APP_INITIALIZER, useFactory: launchAppConfig, deps: [HostService, HttpClient], multi: true},
    LoaderService,
    GetImagePipe,
    ModelService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
