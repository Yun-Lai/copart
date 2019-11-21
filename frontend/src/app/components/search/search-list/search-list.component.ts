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
  selector: 'app-search-list',
  templateUrl: './search-list.component.html',
  styleUrls: [
    './search-list.component.scss'
  ],
  encapsulation: ViewEncapsulation.None,
})
export class SearchListComponent implements OnInit {

  filter_word = '';
  @Input() applied_filter_source: any;
  @Input() applied_sold: any;
  @Input() applied_filter_features = [];
  @Input() applied_filter_makes = [];
  @Input() applied_filter_models = [];
  @Input() applied_filter_years = [];
  @Input() applied_filter_odometers = [];
  @Input() applied_filter_locations = [];
  @Input() applied_filter_sale_dates = [];
  @Input() applied_filter_engine_types = [];
  @Input() applied_filter_transmissions = [];
  @Input() applied_filter_drive_trains = [];
  @Input() applied_filter_cylinders = [];
  @Input() applied_filter_fuels = [];
  @Input() applied_filter_body_styles = [];
  @Input() applied_filter_vehicle_types = [];
  @Input() applied_filter_damages = [];
  @Input() applied_filter_doctypes = [];
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
  // lots = [{"bid_status": "NEVER BID", "info": {"lot": 28920229, "vin": "3PCAJ5M12KF103362", "name": "2019 INFINITI QX50 ESSENTIAL", "type": "V", "make": "INFINITI", "model": "QX50 ESSEN", "year": 2019, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX133/846628de-db98-4e9c-be45-18a51ceb81e5.JPG", "source": true, "doc_type_ts": "FL", "doc_type_stt": "RT", "doc_type_td": "CERT OF TITLE-REBUILT (P)", "odometer_orr": 6929, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "NORMAL WEAR", "lot_2nd_damage": "", "retail_value": 53320, "body_style": "", "color": "RED", "engine_type": "2.0L  4", "cylinders": "4", "transmission": "", "drive": "Front-wheel Drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "FL - MIAMI NORTH", "lane": "", "item": "0", "grid": "*OFF", "images": "PIX133/c793d005-67cc-4bf3-bce0-3e53e6069a15.JPG|PIX133/23e25a33-baab-4e70-8088-33d2e01cd261.JPG|PIX133/992b0439-c5f2-4341-a503-432ad449a333.JPG|PIX133/2c419498-066a-4490-a506-054debaa4d54.JPG|PIX133/a42cec87-3aa7-4911-bd61-bdb938e111dd.JPG|PIX133/f341515e-bb6b-492a-a837-6640e3c8f05b.JPG|PIX133/8b11e1ab-077d-4ffc-86b9-afe64693a622.JPG|PIX133/f9a41d21-5fd0-495b-83f9-e73477d26804.JPG|PIX133/852dabf4-09e6-4091-990e-5f0d9acb0711.JPG|PIX133/367fa9d7-aecb-46ea-b8ed-f0d1f95a5b7b.JPG", "thumb_images": "PIX133/846628de-db98-4e9c-be45-18a51ceb81e5.JPG|PIX133/7d3d25c9-a3d2-4efe-ad84-8cad6408d315.JPG|PIX133/f570c472-bbf4-4957-b066-b44fdcdf8d67.JPG|PIX133/51e5e671-f122-4fd1-b3a3-489350b1926c.JPG|PIX133/86a88cf8-1af7-41ae-a692-c711f5e23c93.JPG|PIX133/f70f94c4-527c-4d2d-951a-927d5f0ae102.JPG|PIX133/600d66ed-ecf0-4f76-b2e5-887d8debda68.JPG|PIX133/34624112-a396-4619-95b0-1c5be813a8ca.JPG|PIX133/cd459f74-0d06-4fa5-9e1e-c6ae5f171106.JPG|PIX133/b7bc7fb5-fc26-41c4-998f-edaa9c10d49b.JPG"}, "sale_status": "MINIMUM BID", "current_bid": 8100, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-04-30T14:00:00Z", "last_update": "2019-03-27T19:09:32Z", "created_at": "2019-03-28T16:18:54.363Z", "updated_at": "2019-03-29T16:29:03.421Z"}, {"bid_status": "NEVER BID", "info": {"lot": 36164609, "vin": "5XXGT4L39KG296916", "name": "2019 KIA OPTIMA LX", "type": "V", "make": "KIA", "model": "OPTIMA LX", "year": 2019, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX148/61548148-b003-4e1f-b53e-ab862fc30782.JPG", "source": true, "doc_type_ts": "NJ", "doc_type_stt": "SC", "doc_type_td": "CERT OF TITLE-SALVAGE", "odometer_orr": 8151, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "SIDE", "lot_2nd_damage": "", "retail_value": 28546, "body_style": "", "color": "BLACK", "engine_type": "2.4L  4", "cylinders": "4", "transmission": "", "drive": "Front-wheel Drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "NJ - SOMERVILLE", "lane": "B", "item": "2021", "grid": "*OFF", "images": "PIX148/0aef6d9d-0607-4cb4-9a20-081d24b9262c.JPG|PIX148/eb133582-6d4f-40a0-8f8d-44c8a18b8eaa.JPG|PIX148/44d3ee57-fa4a-47e1-8519-89bd2bc4cf7c.JPG|PIX148/87d3da62-f707-427d-9b29-f1554648d446.JPG|PIX148/7aae53e2-413c-4732-a04c-fb65ff3c939c.JPG|PIX148/22530d14-34e6-47ac-91bf-4eb6451fa690.JPG|PIX148/eba2bbbb-8bae-4bd0-87ae-a1e8b2392a44.JPG|PIX148/eeb3a73f-a0bc-42cd-86d8-1938c12f1fbd.JPG|PIX148/565de877-d441-4e03-9ee4-209cd764325f.JPG|PIX151/0a95d629-d0a5-43e6-8b0e-b23b267563aa.JPG", "thumb_images": "PIX148/61548148-b003-4e1f-b53e-ab862fc30782.JPG|PIX148/ccda7c2d-8d56-4430-99fe-ebc21d4c58ed.JPG|PIX148/c560b5d9-0db1-45b2-87d0-a185ade0cce6.JPG|PIX148/c4293f8f-8718-4cb4-85b7-f3bcd1c17373.JPG|PIX148/872d8dfb-2b3d-44e4-8da4-bc3d557105f9.JPG|PIX148/0a7a25c6-bfe7-4e23-bd80-e41c54af8eb0.JPG|PIX148/93eebb86-67bb-445f-8ef4-50fa6b7eca01.JPG|PIX148/99e0d21c-a9f9-4bcb-b314-406d5dddeeeb.JPG|PIX148/f9308be1-6582-4dcf-acd6-bf6ecac71b11.JPG|PIX151/3c316876-348c-4941-a89c-d3ac1debcc50.JPG"}, "sale_status": "MINIMUM BID", "current_bid": 7200, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-30T01:00:00Z", "last_update": "2019-05-24T16:35:27Z", "created_at": "2019-05-25T05:17:05.565Z", "updated_at": "2019-05-25T05:17:05.565Z"}, {"bid_status": "NEVER BID", "info": {"lot": 36915819, "vin": "2T1BURHE9KC217458", "name": "2019 TOYOTA COROLLA L", "type": "V", "make": "TOYOTA", "model": "COROLLA L", "year": 2019, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX151/60b76afb-ebd2-4efd-a137-e7600ae7b945.JPG", "source": true, "doc_type_ts": "NJ", "doc_type_stt": "FS", "doc_type_td": "CERT OF TITLE-SALVAGE FLOOD", "odometer_orr": 5, "odometer_ord": "ACTUAL", "lot_highlights": "O", "lot_seller": "", "lot_1st_damage": "WATER/FLOOD", "lot_2nd_damage": "", "retail_value": 24689, "body_style": "", "color": "WHITE", "engine_type": "1.8L  4", "cylinders": "4", "transmission": "", "drive": "Front-wheel Drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "NJ - SOMERVILLE", "lane": "B", "item": "2521", "grid": "*OFF", "images": "PIX151/3c96947b-bc1b-4ae2-83c5-dc15f09e8de3.JPG|PIX151/92a9a781-4949-4886-bd0e-d9edc20b0357.JPG|PIX151/7e198f37-caa5-4d60-a99f-09cf23165364.JPG|PIX151/a3eb276c-b7bc-47ff-bb6e-eefcf2abe750.JPG|PIX151/309f0799-1977-4cbc-a6ef-c0e29ec6d476.JPG|PIX151/6cd7e023-5d49-4d22-9d96-0e4a2e38dcd7.JPG|PIX151/15cb0eb6-1b3e-47b8-99ec-019db11cc4d7.JPG|PIX151/7b9ca774-97fd-406f-a305-ca89e8541a1c.JPG|PIX151/8bb57c10-e550-45c5-b2c7-ab823614f293.JPG|PIX151/590a32f1-cf24-4eff-b464-1fa88545d4c0.JPG", "thumb_images": "PIX151/60b76afb-ebd2-4efd-a137-e7600ae7b945.JPG|PIX151/d0e01642-8dc9-4f01-9fd6-22f7f37182d6.JPG|PIX151/7b53e765-ddc0-481a-83bc-630ad50c1ac4.JPG|PIX151/ea6cbd14-d528-4358-b6a6-b599b1f687f2.JPG|PIX151/a0ceab09-cecc-4c18-9d32-11f3fa379eef.JPG|PIX151/b98f9365-6070-48a4-9f96-55c81bbbbb34.JPG|PIX151/ac8d90a5-0930-4f1c-b66e-e9b895974cbb.JPG|PIX151/a391b573-8b65-4422-b0a4-d9484e603f71.JPG|PIX151/248432d9-84ba-4423-9964-4f3c6776f236.JPG|PIX151/74afe231-5ab4-40a5-b192-977b5b4d1502.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 11700, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-30T01:00:00Z", "last_update": "2019-05-24T14:05:26Z", "created_at": "2019-05-25T05:38:19.974Z", "updated_at": "2019-05-25T05:38:19.974Z"}, {"bid_status": "NEVER BID", "info": {"lot": 30920489, "vin": "1C4PJMBX4KD216779", "name": "2019 JEEP CHEROKEE TRAILHAWK", "type": "V", "make": "JEEP", "model": "CHEROKEE T", "year": 2019, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX133/f61079f7-cfda-4abe-b75c-11f9101df171.JPG", "source": true, "doc_type_ts": "IN", "doc_type_stt": "RT", "doc_type_td": "CERT OF TITLE - REBUILT VEHICL (P)", "odometer_orr": 34, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "WATER/FLOOD", "lot_2nd_damage": "", "retail_value": 40505, "body_style": "", "color": "GRAY", "engine_type": "3.2L  6", "cylinders": "6", "transmission": "", "drive": "4x4 w/Front Whl Drv", "fuel": "FLEXIBLE FUEL", "keys": "YES", "notes": "", "location": "IL - WHEELING", "lane": "A", "item": "73", "grid": "*OFF", "images": "PIX133/8e43f920-19c7-4dce-a618-4702577da1eb.JPG|PIX133/faa23e05-3c38-415d-a0c3-a88d78cc7811.JPG|PIX133/a0f31278-06f9-45e1-8545-700f2eb1130d.JPG|PIX133/a7d77093-5773-4801-8fdf-27af5e4586ed.JPG|PIX133/d6821e5a-37e2-4e83-8649-68a598d8d9b6.JPG|PIX133/fb55b001-7ba6-4685-abda-01a5a3729f0c.JPG|PIX133/62ef80d6-6187-4c53-a131-49adabe91a85.JPG|PIX133/d706cbbf-47bc-4dcc-b8c1-05b1256b6788.JPG|PIX133/8802ff43-bde5-42aa-924b-e267a0f39207.JPG", "thumb_images": "PIX133/f61079f7-cfda-4abe-b75c-11f9101df171.JPG|PIX133/76dd2561-ac20-43b7-8959-61a8006cc4c3.JPG|PIX133/67365cfa-3bbc-485f-92ad-21b19caee54a.JPG|PIX133/e51ba2d3-76bb-49c4-85ff-7e60fbab97ef.JPG|PIX133/991d1a8d-1a69-4715-bb03-ba6ed60589fb.JPG|PIX133/7b72241b-d50f-4e50-8ce9-f0f73d8db52e.JPG|PIX133/2fd049bf-2dd4-4ac9-891d-a1141ec2f32c.JPG|PIX133/3d50e6bb-e747-4049-96ce-4f96564b8c3d.JPG|PIX133/575109db-ebdb-4bef-87bc-69cc21942071.JPG"}, "sale_status": "MINIMUM BID", "current_bid": 0, "buy_today_bid": 17100, "sold_price": 0, "sale_date": "2019-04-22T17:00:00Z", "last_update": "2019-04-12T02:28:22Z", "created_at": "2019-04-12T07:19:04.712Z", "updated_at": "2019-04-12T07:19:04.712Z"}, {"bid_status": "NEVER BID", "info": {"lot": 35418309, "vin": "5TDYZ3DC0KS985379", "name": "2019 TOYOTA SIENNA LIMITED", "type": "V", "make": "TOYOTA", "model": "SIENNA LIM", "year": 2019, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX145/813b8c4c-fbfc-443f-98b0-1ec9bcbd5102.JPG", "source": true, "doc_type_ts": "NJ", "doc_type_stt": "FS", "doc_type_td": "CERT OF TITLE-SALVAGE FLOOD", "odometer_orr": 1, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "WATER/FLOOD", "lot_2nd_damage": "", "retail_value": 40002, "body_style": "", "color": "SILVER", "engine_type": "3.5L  6", "cylinders": "6", "transmission": "", "drive": "Front-wheel Drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "NJ - SOMERVILLE", "lane": "", "item": "0", "grid": "*OFF", "images": "PIX145/304c4aab-eb62-4a69-bdd3-9cd672307ffc.JPG|PIX145/d2470d8c-211b-4432-a026-29307e621337.JPG|PIX145/57614ea6-7a4c-4f9c-8fbf-570e03391ea3.JPG|PIX145/94d9dfd8-364d-45ef-a1a5-1bd490cd9f64.JPG|PIX145/32d84ec5-7f1f-412c-9348-55f177d605cb.JPG|PIX145/9ccb8342-81b4-4b84-b883-9db9d6594e48.JPG|PIX145/b3597c24-d39e-4f06-9b3e-da5e923e4141.JPG|PIX145/d30c7251-a18c-463f-98a7-a401caad41e9.JPG|PIX145/10b6e87c-8f51-4f69-b9bc-b98eaa679c54.JPG|PIX145/960db668-857e-47be-9d0a-d6ca403eaf91.JPG", "thumb_images": "PIX145/813b8c4c-fbfc-443f-98b0-1ec9bcbd5102.JPG|PIX145/9c201f15-bcf0-448e-99ba-462008809075.JPG|PIX145/bba5744e-9c7a-4ad3-9e9c-10b0009e29a8.JPG|PIX145/e2911077-71b5-4888-878d-ced8d84b0745.JPG|PIX145/effb8301-76fa-4b39-8d62-5887d9a910ae.JPG|PIX145/42f453ab-cd6e-48f8-93fb-c3ed7fcec0b0.JPG|PIX145/96fb439b-3579-4184-9ac2-77ed907ebc7d.JPG|PIX145/0cd4294f-ee31-4715-be54-3f85f8740d15.JPG|PIX145/993fc035-cc89-4820-b623-8453e442a4f8.JPG|PIX145/699e76c1-2768-4d6f-9517-0083baa837a8.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 21600, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-30T01:00:00Z", "last_update": "2019-05-24T15:29:42Z", "created_at": "2019-05-25T05:37:55.540Z", "updated_at": "2019-05-25T05:37:55.540Z"}, {"bid_status": "NEVER BID", "info": {"lot": 34612469, "vin": "5TDBZRFH5KS947339", "name": "2019 TOYOTA HIGHLANDER LE", "type": "V", "make": "TOYOTA", "model": "HIGHLANDER", "year": 2019, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX142/ce2c8265-a4e8-414e-8f02-e3a6fc1e2d1f.JPG", "source": true, "doc_type_ts": "NJ", "doc_type_stt": "FS", "doc_type_td": "CERT OF TITLE-SALVAGE FLOOD", "odometer_orr": 5, "odometer_ord": "ACTUAL", "lot_highlights": "OS", "lot_seller": "", "lot_1st_damage": "WATER/FLOOD", "lot_2nd_damage": "", "retail_value": 35876, "body_style": "", "color": "BLACK", "engine_type": "3.5L  6", "cylinders": "6", "transmission": "", "drive": "All wheel drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "NJ - SOMERVILLE", "lane": "C", "item": "3082", "grid": "*OFF", "images": "PIX142/13d232a2-09de-4b9c-a88c-5275543bc733.JPG|PIX142/c3c3bf59-7016-4ae1-92c5-28c81773c55f.JPG|PIX142/102fd955-4992-42b8-bb36-1cfbb1e1a59f.JPG|PIX142/36e3d885-09b1-4d98-b33f-79d84b3cb3b5.JPG|PIX142/17c867c9-00b3-4430-bab0-9a7057da78ba.JPG|PIX142/58ed0734-ea2f-49bf-b24c-0d87fc50317c.JPG|PIX142/ae1cc13b-4ff0-4fe7-b24a-bdfbdca805f6.JPG|PIX142/07bb6443-2579-45b7-8170-8b4cfda634d9.JPG|PIX142/8e9e97a3-f329-4c03-a5ea-b10094e3e75d.JPG|PIX142/8210f7a3-9cbb-44ff-93d4-72f357359ec3.JPG", "thumb_images": "PIX142/ce2c8265-a4e8-414e-8f02-e3a6fc1e2d1f.JPG|PIX142/b895d931-768d-4794-8200-6fca68a999a9.JPG|PIX142/8e01c0da-1a4b-4650-8d02-5cb76223af31.JPG|PIX142/d9594867-2230-42c7-bb6e-37ff017772c8.JPG|PIX142/0f975b4f-e33c-45fe-9f4b-0aa39c0bc74d.JPG|PIX142/c58ba893-97b5-4177-9908-d7bc431466d8.JPG|PIX142/324f9ff8-9b21-405f-9d0a-84613c33bdfe.JPG|PIX142/12f36183-6eed-436c-9c92-10d548d59059.JPG|PIX142/997f3b2d-0242-411c-b275-351a4d6fb5af.JPG|PIX142/ae98aa81-6570-48f0-a084-0b4c26e3405d.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 20200, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-30T01:00:00Z", "last_update": "2019-05-24T16:19:21Z", "created_at": "2019-05-25T05:37:46.876Z", "updated_at": "2019-05-25T05:37:46.876Z"}, {"bid_status": "NEVER BID", "info": {"lot": 31738799, "vin": "5TDJZRFH1KS936513", "name": "2019 TOYOTA HIGHLANDER SE", "type": "V", "make": "TOYOTA", "model": "HIGHLANDER", "year": 2019, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX133/f034c541-9343-48c9-a665-8ec8d6e4f002.JPG", "source": true, "doc_type_ts": "NJ", "doc_type_stt": "FS", "doc_type_td": "CERT OF TITLE-SALVAGE FLOOD", "odometer_orr": 3, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "WATER/FLOOD", "lot_2nd_damage": "", "retail_value": 42547, "body_style": "", "color": "WHITE", "engine_type": "3.5L  6", "cylinders": "6", "transmission": "", "drive": "All wheel drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "NJ - SOMERVILLE", "lane": "B", "item": "2051", "grid": "*OFF", "images": "PIX133/6f57962c-4958-412f-8142-3706db5e2783.JPG|PIX133/24a37b59-573d-46a4-9aa5-9c2b1a15d43c.JPG|PIX133/53a29704-4236-4c93-9290-f86b60fb1824.JPG|PIX133/f953f03a-2166-473d-a0b9-8d44768a507a.JPG|PIX133/2c45ee45-eeb8-49f4-8f7a-9421127fc354.JPG|PIX133/73ee82cd-473f-46fd-bde0-d815087772dc.JPG|PIX133/642543c0-4608-4bac-b6e2-5f2374fee732.JPG|PIX133/2cd10abf-f9a6-4dd5-9c00-cddfdef57465.JPG|PIX133/f353297e-918c-4a70-9ef5-1589811dee6f.JPG|PIX133/ee7baf58-6767-4648-b6d2-4574bd9c56da.JPG", "thumb_images": "PIX133/f034c541-9343-48c9-a665-8ec8d6e4f002.JPG|PIX133/32398c7a-21c1-41e9-ac1b-51a0425c81d4.JPG|PIX133/c11dee83-ccea-4af5-a463-94f25ab68ccf.JPG|PIX133/11579a8a-0043-426e-9355-f926dc3e9299.JPG|PIX133/778275ca-2cb5-400a-bec4-53f31e3cb611.JPG|PIX133/d423e89d-98b2-476a-8bd2-407fe39d2ec3.JPG|PIX133/3701985a-5601-4a95-ac16-c19e64e9500b.JPG|PIX133/bbb941e4-0d84-4df4-9634-891fe04c409f.JPG|PIX133/5d34f45d-5fa7-4a69-a0be-9addfa07d672.JPG|PIX133/9e6c19bc-8de5-4d4d-8e46-9aefb3edf38b.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 5600, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-03T14:00:00Z", "last_update": "2019-04-25T18:15:33Z", "created_at": "2019-04-25T12:42:26.783Z", "updated_at": "2019-04-26T12:39:27.022Z"}, {"bid_status": "NEVER BID", "info": {"lot": 53268568, "vin": "JTMHV01JXK5042855", "name": "2019 TOYOTA LAND CRUIS", "type": "V", "make": "TOYOTA", "model": "LAND CRUIS", "year": 2019, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX133/6f089d8e-4188-437d-9ad7-77a1f80fd64f.JPG", "source": true, "doc_type_ts": "FL", "doc_type_stt": "CO", "doc_type_td": "CERTIFICATE OF ORIGIN (P)", "odometer_orr": 50, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "NORMAL WEAR", "lot_2nd_damage": "", "retail_value": 86400, "body_style": "", "color": "BLACK", "engine_type": "", "cylinders": "", "transmission": "", "drive": "", "fuel": "", "keys": "YES", "notes": "", "location": "FL - MIAMI CENTRAL", "lane": "B", "item": "2061", "grid": "*OFF", "images": "PIX133/bc6dfa11-d545-42b0-aa94-a00970f925f9.JPG|PIX133/d0f61ecd-97ff-4797-9aa0-7a3336675cc8.JPG|PIX133/55c112b4-b3f0-499b-abce-aba4079fbf05.JPG|PIX133/9ee7c138-eee4-4efe-a9e5-fcee7df3cbef.JPG|PIX133/75c87469-f23e-4648-9ced-f7ac40fcba5d.JPG|PIX133/2c61d604-b0c0-4668-a0e8-55d638475b91.JPG|PIX133/e7757a01-52d6-4313-9955-75cdf08a0277.JPG|PIX133/07f27837-5884-4473-8363-0b48be63966a.JPG|PIX133/b792b202-7508-4779-92cc-8c068f1af767.JPG|PIX133/c2411100-6ce0-4e3c-83a2-f65739cf9b5e.JPG", "thumb_images": "PIX133/6f089d8e-4188-437d-9ad7-77a1f80fd64f.JPG|PIX133/368065d2-08f4-4ab8-9338-aae6366b8fed.JPG|PIX133/0bb226da-53f3-40c1-8802-cf20c38c4d2e.JPG|PIX133/c08dee2c-2321-44c4-b24e-ae82791044eb.JPG|PIX133/e1678084-fb2a-42fb-a2ad-7552b30edee3.JPG|PIX133/8d8b0a97-20a7-401d-9cae-d14b4a9cce24.JPG|PIX133/e2b04fc5-5361-456a-a9dd-0e23ef59861b.JPG|PIX133/46ad97bd-0e59-4d3f-8d72-5912803316fd.JPG|PIX133/e25221b2-7f18-4c34-a47c-e60a83cfe760.JPG|PIX133/3d3a910c-f3e8-475d-bcd4-a825eae70e32.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 10100, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-30T14:00:00Z", "last_update": "2019-05-23T11:04:21Z", "created_at": "2019-05-23T06:24:28.991Z", "updated_at": "2019-05-25T05:45:28.435Z"}, {"bid_status": "NEVER BID", "info": {"lot": 36293569, "vin": "WDCTG4GB6JJ419614", "name": "2018 MERCEDES-BENZ GLA 250 4MATIC", "type": "V", "make": "MERCEDES-BENZ", "model": "GLA 250 4M", "year": 2018, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX148/77bf4da2-98c6-477e-8eed-10e3241504a4.JPG", "source": true, "doc_type_ts": "NJ", "doc_type_stt": "FS", "doc_type_td": "CERT OF TITLE-SALVAGE FLOOD", "odometer_orr": 33460, "odometer_ord": "ACTUAL", "lot_highlights": "O", "lot_seller": "", "lot_1st_damage": "WATER/FLOOD", "lot_2nd_damage": "", "retail_value": 39597, "body_style": "", "color": "BLUE", "engine_type": "2.0L  4", "cylinders": "4", "transmission": "", "drive": "All wheel drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "NJ - SOMERVILLE", "lane": "C", "item": "3007", "grid": "*OFF", "images": "PIX148/f9ac93f2-437e-4435-8815-509dd698ff01.JPG|PIX148/90da335b-ef3c-4a63-bae9-67be9d7c55a5.JPG|PIX148/f8e16f87-0bef-4421-8b58-58a3171f530e.JPG|PIX148/8a69a905-46ba-405a-a83e-e56ddf4bc793.JPG|PIX148/c0ce0b68-be19-4a9d-a065-149d0b870a40.JPG|PIX148/2d5a9b52-ffaf-4d02-8b80-dfb8d579c5e4.JPG|PIX148/7f58a51d-f618-401a-baba-f0e932cd83e3.JPG|PIX148/9804b6c8-9e35-424f-aa04-3c68684ff5d7.JPG|PIX148/ce529fc6-21c3-40f5-91ef-effc15b4485c.JPG|PIX148/be273137-6eac-4c25-a4b1-e035fd89bf61.JPG", "thumb_images": "PIX148/77bf4da2-98c6-477e-8eed-10e3241504a4.JPG|PIX148/12e5a7e2-ff88-4d59-974d-15bda655b579.JPG|PIX148/50f99830-2eda-4721-af7c-7e489baf9051.JPG|PIX148/9663b966-6149-457d-b7ed-da4243c7407f.JPG|PIX148/63bdf7ad-f812-420d-a0ed-be7fc312d586.JPG|PIX148/3ede20d7-b403-40c5-b69b-08f6fa586a42.JPG|PIX148/0d3187d8-1711-41a7-8e6b-f03eefaa914f.JPG|PIX148/ebf10fed-cec0-4a33-b223-eb3432ae5f73.JPG|PIX148/91b5685e-d650-4ba4-ad91-6e29c0052c1b.JPG|PIX148/56b53bf2-de52-4dc5-b731-f8c26926a01e.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 13400, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-30T01:00:00Z", "last_update": "2019-05-24T16:19:38Z", "created_at": "2019-05-25T05:49:05.469Z", "updated_at": "2019-05-25T05:49:05.469Z"}, {"bid_status": "NEVER BID", "info": {"lot": 34355849, "vin": "4JGED6EB6JA110422", "name": "2018 MERCEDES-BENZ GLE COUPE 43 AMG", "type": "V", "make": "MERCEDES-BENZ", "model": "GLE COUPE", "year": 2018, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX141/c25e16c6-4478-465d-bb09-c25668f5b131.JPG", "source": true, "doc_type_ts": "NJ", "doc_type_stt": "CT", "doc_type_td": "CERTIFICATE OF TITLE (P)", "odometer_orr": 6274, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "FRONT END", "lot_2nd_damage": "", "retail_value": 83567, "body_style": "", "color": "WHITE", "engine_type": "3.0L  6", "cylinders": "6", "transmission": "", "drive": "All wheel drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "NJ - SOMERVILLE", "lane": "", "item": "0", "grid": "*OFF", "images": "PIX141/32c4dde5-f22f-4071-b4e0-4a6d320606fd.JPG|PIX141/45095375-b07f-44a5-b536-c939c3ae056e.JPG|PIX141/9ecc4957-7761-4dc3-addb-3a2836a6de75.JPG|PIX141/5f1a8fb9-3d06-4d61-b5bc-c5ecb880388e.JPG|PIX141/2ee4af44-4ba4-4dc1-829a-51ba641c54f5.JPG|PIX141/97f3698f-6a23-45ec-abfb-c929e8011b7a.JPG|PIX141/8e4cd9f3-198b-492b-9493-c809d1314565.JPG|PIX141/b62cdec1-8d08-495e-bc8f-698e9fe8882f.JPG|PIX141/b43a123d-ff78-452b-a80a-e85426c9ee3c.JPG|PIX141/b8ecb1e7-1715-4a58-b75c-5291070dc931.JPG", "thumb_images": "PIX141/c25e16c6-4478-465d-bb09-c25668f5b131.JPG|PIX141/44a6a6af-b4ea-449d-a2be-90c6183ef2d4.JPG|PIX141/867133a9-8ef6-4a87-99bb-6f1108f0aa97.JPG|PIX141/dd62681d-48a3-451d-a10d-853852bbdbbc.JPG|PIX141/9a4e422f-6bee-4a26-b162-757d2f8b7752.JPG|PIX141/abcc4336-6207-4de4-bff8-66ad0fbbd67e.JPG|PIX141/edb4822b-ef6e-4715-a2b1-47a498cc5cd8.JPG|PIX141/8215dcfa-b4ea-4fa3-8d2e-b722ded47c50.JPG|PIX141/72766703-d3e8-4525-8af6-fd7effbc227f.JPG|PIX141/2c3443ed-8100-4a88-a5c1-5aa5e78a1207.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 43250, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-30T01:00:00Z", "last_update": "2019-05-24T14:32:52Z", "created_at": "2019-05-25T05:48:49.782Z", "updated_at": "2019-05-25T05:48:49.782Z"}, {"bid_status": "NEVER BID", "info": {"lot": 29952819, "vin": "2FMPK3K98JBB20405", "name": "2018 FORD EDGE TITANIUM", "type": "V", "make": "FORD", "model": "EDGE TITAN", "year": 2018, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX133/3aece632-9cdf-4278-9a08-211744e7f20b.JPG", "source": true, "doc_type_ts": "SC", "doc_type_stt": "CT", "doc_type_td": "CERTIFICATE OF TITLE (P)", "odometer_orr": 31173, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "NORMAL WEAR", "lot_2nd_damage": "", "retail_value": 25000, "body_style": "", "color": "GRAY", "engine_type": "2.0L  4", "cylinders": "4", "transmission": "", "drive": "Front-wheel Drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "MO - SIKESTON", "lane": "A", "item": "55", "grid": "*OFF", "images": "PIX133/3ece4f81-b94d-4a83-97dd-c4d41f2edcff.JPG|PIX133/8b7cf063-6aa3-468b-8064-373100373406.JPG|PIX133/c59d5d5e-d3a6-44ad-87fd-cb20fea1de31.JPG|PIX133/02e08361-f54e-46fd-977e-57bb98846f14.JPG|PIX133/62602a26-f725-4858-acef-909a5ad11e6f.JPG|PIX133/8369536d-7cbb-4b25-8ba9-e0f712b8832e.JPG|PIX133/8a324db7-4d32-46a2-9bcc-f8d9836c58a9.JPG|PIX133/92be471c-eefa-49ea-808b-8a09b4353326.JPG|PIX133/7629ef8b-a50b-4d0e-9598-5315f2d1e05b.JPG", "thumb_images": "PIX133/3aece632-9cdf-4278-9a08-211744e7f20b.JPG|PIX133/6ef1cfd9-47c3-4f33-be50-be6c924c11c5.JPG|PIX133/7a71a7ab-dd21-48bb-b610-69513e836631.JPG|PIX133/764c0e51-8ce4-45f9-9293-28daa7954c99.JPG|PIX133/6b49955c-6872-464c-96d7-d5afadecc5bd.JPG|PIX133/0cb97b2c-b78f-4768-af08-ad82a07dc19d.JPG|PIX133/011a2314-fe14-46e3-ad72-c6821ce356d1.JPG|PIX133/7e01322f-a697-457b-b3b1-dbee78fc2ba6.JPG|PIX133/42bee5c0-ee93-4322-a0b1-a45e608a2dbc.JPG"}, "sale_status": "MINIMUM BID", "current_bid": 0, "buy_today_bid": 17000, "sold_price": 0, "sale_date": "2019-04-08T17:00:00Z", "last_update": "2019-04-02T15:48:26Z", "created_at": "2019-03-29T08:52:57.940Z", "updated_at": "2019-04-04T08:08:11.139Z"}, {"bid_status": "NEVER BID", "info": {"lot": 27737409, "vin": "WVGBV7AX3JK004690", "name": "2018 VOLKSWAGEN TIGUAN LIMITED ", "type": "V", "make": "VOLKSWAGEN", "model": "TIGUAN LIM", "year": 2018, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX133/a8469b68-1199-4410-9e71-f458d39363dd.JPG", "source": true, "doc_type_ts": "NJ", "doc_type_stt": "SC", "doc_type_td": "CERT OF TITLE-SALVAGE (P)", "odometer_orr": 1014, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "FRONT END", "lot_2nd_damage": "", "retail_value": 29564, "body_style": "", "color": "GRAY", "engine_type": "2.0L  4", "cylinders": "4", "transmission": "", "drive": "All wheel drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "NJ - SOMERVILLE", "lane": "", "item": "0", "grid": "*OFF", "images": "PIX133/ce32d452-c8a6-43f5-83bd-e86ec142d515.JPG|PIX133/3a9dfadc-2741-4357-920b-f3e924cfe458.JPG|PIX133/5ef35425-993c-49da-80f5-fb99da81b145.JPG|PIX133/26cb1981-b73e-41b4-ab6a-f96981c9fcd7.JPG|PIX133/de62935a-e7f1-481d-a637-4b12d61c71dd.JPG|PIX133/092f6e03-599f-49d7-b525-d221be028d6b.JPG|PIX133/3531283f-2957-48e3-8ea7-35b9094b9682.JPG|PIX133/76f7c249-2c6b-491b-96aa-6ae054e98a47.JPG|PIX133/2c33a689-9cc4-4c11-8d5b-2ec4c061eace.JPG|PIX133/f47c01ab-9c9f-4d26-b088-cc28ea8b2eeb.JPG", "thumb_images": "PIX133/a8469b68-1199-4410-9e71-f458d39363dd.JPG|PIX133/bef29171-fdca-40df-994a-41544916c2b1.JPG|PIX133/22fe7cb8-e88e-45f3-a522-9ccc03e5d240.JPG|PIX133/2ca6fbfb-ce70-4362-96e4-c5d2bfe30acb.JPG|PIX133/2103e9df-bee5-4b33-b157-0b1b10872237.JPG|PIX133/84d6fefb-0ada-4a71-8adf-346d27dd7bfd.JPG|PIX133/5cea24ef-506e-47a7-b85c-0d13cd756844.JPG|PIX133/5a6336a7-a63a-4f49-9dab-d69783128427.JPG|PIX133/fcfbb079-b9d3-4b5f-b8fa-ba15859dca0b.JPG|PIX133/fcb434f6-e2a2-4cd3-be0a-80a891cac367.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 1700, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-02-22T15:00:00Z", "last_update": "2019-02-20T18:44:47Z", "created_at": "2019-02-21T05:21:33.322Z", "updated_at": "2019-02-21T05:21:33.322Z"}, {"bid_status": "NEVER BID", "info": {"lot": 34493799, "vin": "ZFF79ALA4J0229508", "name": "2018 FERRARI 488 GTB ", "type": "V", "make": "FERRARI", "model": "488 GTB", "year": 2018, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX145/5eebd089-3bbc-40c4-9f2e-b0592819e746.JPG", "source": true, "doc_type_ts": "FL", "doc_type_stt": "RB", "doc_type_td": "CERT OF TITLE SLVG REBUILDABLE (P)", "odometer_orr": 0, "odometer_ord": "NOT ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "FRONT END", "lot_2nd_damage": "", "retail_value": 348896, "body_style": "", "color": "GRAY", "engine_type": "3.9L  8", "cylinders": "8", "transmission": "", "drive": "Rear-wheel drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "FL - MIAMI SOUTH", "lane": "", "item": "0", "grid": "*OFF", "images": "PIX145/5e75f89d-33ec-4ed7-93c5-a9b7473408d1.JPG|PIX145/a31e60bd-737a-425e-bfef-eb8ce89724d5.JPG|PIX145/04e8c6c2-7d87-44aa-a184-7cf5408f3d39.JPG|PIX145/d68f6c58-1922-4d42-9acc-351c3d5465a3.JPG|PIX145/55803445-33b2-4d9d-a005-23f0e245e23a.JPG|PIX145/df844e1c-7067-464f-bb1a-59b676c3a1a9.JPG|PIX145/d0bafc46-4121-4200-bd09-930f8d95e2b0.JPG|PIX145/6fb8ea30-43a7-425e-bc45-42a80c5d835f.JPG|PIX145/c5d80fbc-f06b-4fdc-8966-2d2e68d6dffd.JPG|PIX145/2686fb32-ffa5-4177-a592-26bae9def14c.JPG", "thumb_images": "PIX145/5eebd089-3bbc-40c4-9f2e-b0592819e746.JPG|PIX145/d64aa7ef-496b-4138-a8c1-9b38d400cdcf.JPG|PIX145/8dcf3752-9a0b-4b1b-b6ec-0cbaf4f7b58f.JPG|PIX145/404eea1d-5d9e-42a2-a528-2d8c7c06482b.JPG|PIX145/085ebd3d-3946-4083-8ff6-fd2d882da90c.JPG|PIX145/5b4e0b05-5877-47e6-9e9b-d028ecb249bf.JPG|PIX145/22e73cac-df92-45ce-b71e-524ae5c1a2d6.JPG|PIX145/ce916d80-d320-441d-88a6-2b1ef10109a9.JPG|PIX145/96e945b7-a80b-417f-b1f1-50bef0e36016.JPG|PIX145/ef49d1cd-7032-460b-b959-bc810d9e0b60.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 168000, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-29T01:00:00Z", "last_update": "2019-05-24T03:02:18Z", "created_at": "2019-05-24T07:10:15.414Z", "updated_at": "2019-05-25T06:47:03.967Z"}, {"bid_status": "NEVER BID", "info": {"lot": 36961139, "vin": "1HGCV1F19JA102771", "name": "2018 HONDA ACCORD LX", "type": "V", "make": "HONDA", "model": "ACCORD LX", "year": 2018, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX150/4491e767-21ac-4a70-92b5-7c1b1327e4f2.JPG", "source": true, "doc_type_ts": "TX", "doc_type_stt": "CQ", "doc_type_td": "DLR/DIS/EXP-CT OTHERS-ACQ (P)", "odometer_orr": 9704, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "NORMAL WEAR", "lot_2nd_damage": "", "retail_value": 0, "body_style": "", "color": "BLACK", "engine_type": "1.5L  4", "cylinders": "4", "transmission": "", "drive": "Front-wheel Drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "CA - SACRAMENTO", "lane": "", "item": "0", "grid": "*OFF", "images": "PIX150/3eda4ea6-4aca-470f-8f89-2f28ecd95e7d.JPG|PIX150/21ca4853-7ad7-40d6-a900-c98bcc7e1503.JPG|PIX150/fd324e93-1e68-4c51-995b-27bd8ee0a771.JPG|PIX150/3fe5e2cb-2817-4043-aa22-946426f08617.JPG|PIX150/15405f17-0d2f-4e23-9574-5cebfc953bbe.JPG|PIX150/62cef888-20ea-452f-a47e-94281d8cd7e0.JPG|PIX150/61698154-adac-440a-af28-bd697d7597ad.JPG|PIX150/31d2ee21-4d88-4c12-8393-8373a4cef1b4.JPG|PIX150/a3ee1e4a-9282-43fa-99dc-7a94b1c053ce.JPG|PIX150/4906f329-4840-442e-91c7-55366ab5a87f.JPG", "thumb_images": "PIX150/4491e767-21ac-4a70-92b5-7c1b1327e4f2.JPG|PIX150/87cecd73-6b98-4229-a60e-07cd7685de0b.JPG|PIX150/ea676b6e-0f3f-417a-9786-021cd3bff918.JPG|PIX150/27a5127c-a94d-4685-83fb-d3e7c70896e1.JPG|PIX150/9148b6c6-3850-4332-aba5-3805d71176e4.JPG|PIX150/16efb036-3cfc-442c-a5d1-785e6928012b.JPG|PIX150/dc9ad05d-895d-4add-9e78-38e1972b5508.JPG|PIX150/292eff3b-7b7e-4908-97f9-c8a2b559c9fc.JPG|PIX150/1ef7e2be-c703-4e36-b525-1baa6d778d8c.JPG|PIX150/50ae59ed-7fad-4424-961a-b6b743039366.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 0, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-28T19:00:00Z", "last_update": "2019-05-24T21:51:13Z", "created_at": "2019-05-22T05:44:53.170Z", "updated_at": "2019-05-25T05:25:47.895Z"}, {"bid_status": "NEVER BID", "info": {"lot": 34756389, "vin": "JTMBFREV5JD253292", "name": "2018 TOYOTA RAV4 LE", "type": "V", "make": "TOYOTA", "model": "RAV4 LE", "year": 2018, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX143/def7d0c4-c475-4bb0-b0e2-74bfc4bb2bd7.JPG", "source": true, "doc_type_ts": "NJ", "doc_type_stt": "FS", "doc_type_td": "CERT OF TITLE-SALVAGE FLOOD", "odometer_orr": 45, "odometer_ord": "ACTUAL", "lot_highlights": "OS", "lot_seller": "", "lot_1st_damage": "WATER/FLOOD", "lot_2nd_damage": "", "retail_value": 27016, "body_style": "", "color": "SILVER", "engine_type": "2.5L  4", "cylinders": "4", "transmission": "", "drive": "All wheel drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "NJ - SOMERVILLE", "lane": "C", "item": "3100", "grid": "*OFF", "images": "PIX143/6a037130-f385-4a92-ae8f-fdc8ef862bcd.JPG|PIX143/6bf35a5f-9f7d-4bda-a772-c3b90159d0d5.JPG|PIX143/7f7d3d1c-ac36-4bd1-977d-95200b3778ad.JPG|PIX143/09618739-e4d7-4b49-8487-7847b124ffe5.JPG|PIX143/d8710dae-d4d4-4143-bc9b-5144172cc148.JPG|PIX143/aa4e476d-a1c6-4783-8b9f-51c9c72fa705.JPG|PIX143/d3a2d6db-afca-4d30-b23c-644e26a6b793.JPG|PIX143/da8370ed-deeb-4085-bf0b-c9e538195bbe.JPG|PIX143/30991d30-2c94-4604-8558-a6d9eb585c69.JPG|PIX143/24ad7e70-626d-4c44-ba2e-bf5e21bfe980.JPG", "thumb_images": "PIX143/def7d0c4-c475-4bb0-b0e2-74bfc4bb2bd7.JPG|PIX143/21edd834-e078-469d-8d0f-4bdea702d127.JPG|PIX143/a58a312b-9796-4781-8dd1-d975815bedce.JPG|PIX143/de00fa0c-e8a2-4dcb-b785-26005ddba44d.JPG|PIX143/00d97a50-5ba1-4372-b41f-84d76b840448.JPG|PIX143/c0235cb7-2747-4f43-91b1-048c0d1c6fe2.JPG|PIX143/28962117-8658-40e5-906f-d803e929a689.JPG|PIX143/ca03e895-6c1c-46d2-bb2e-8294aa4ac6b1.JPG|PIX143/439d5a77-1191-43ba-8986-a24a6bedfb30.JPG|PIX143/f80db4e0-0920-4efe-b84c-635c2964d9d5.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 13800, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-30T01:00:00Z", "last_update": "2019-05-24T15:49:09Z", "created_at": "2019-05-25T05:37:47.571Z", "updated_at": "2019-05-25T05:37:47.571Z"}, {"bid_status": "NEVER BID", "info": {"lot": 25395039, "vin": "WDDSJ4GB2JN609959", "name": "2018 MERCEDES-BENZ CLA 250 4MATIC", "type": "V", "make": "MERCEDES-BENZ", "model": "CLA 250 4M", "year": 2018, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX133/8c86d80c-8eb7-4b2a-8dee-6365533fe568.JPG", "source": true, "doc_type_ts": "NJ", "doc_type_stt": "CT", "doc_type_td": "CERTIFICATE OF TITLE (P)", "odometer_orr": 20484, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "MINOR DENT/SCRATCHES", "lot_2nd_damage": "", "retail_value": 0, "body_style": "", "color": "BLACK", "engine_type": "2.0L  4", "cylinders": "4", "transmission": "", "drive": "All wheel drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "CT - HARTFORD", "lane": "B", "item": "2100", "grid": "*OFF", "images": "PIX133/5a8abe08-b162-4f4e-829f-061d04c9fbc0.JPG|PIX133/3c68b135-0fc8-465b-90d1-5870aa1412f4.JPG|PIX133/3c03f535-f4b2-4c5b-aece-b2f539f45166.JPG|PIX133/c3a3a9a7-4449-4d89-bffd-882fe930aa42.JPG|PIX133/9300a7d9-271e-44dd-bfe1-71c47b4e4c17.JPG|PIX133/74a0e065-ddff-4aa8-ad49-7f1c448a0567.JPG|PIX133/9d1240a3-da2e-4008-adc6-bf765ce3f218.JPG|PIX133/da73432b-aef9-478f-97fb-d9756a217ba0.JPG|PIX133/0c2f21ce-4070-4dfb-bc80-0ac373f19326.JPG|PIX133/0f622722-aca0-4931-9d3b-cb1737719969.JPG", "thumb_images": "PIX133/8c86d80c-8eb7-4b2a-8dee-6365533fe568.JPG|PIX133/2ef4c3bb-c889-43b5-8e3a-3ccda3d7811f.JPG|PIX133/ea2cb838-19c1-4a70-9a2b-cff920c26b91.JPG|PIX133/d0be0751-4832-40b0-a9ee-de5f53c8e57a.JPG|PIX133/ef33e71d-af81-4387-aec5-528c3a6d6b1f.JPG|PIX133/6de74c0a-7c46-4522-b030-768740782298.JPG|PIX133/2c4b523c-b5d7-43ee-b0b2-58911d81c330.JPG|PIX133/5387b62c-4092-4154-b183-64b48ace8a1f.JPG|PIX133/2676fb12-05ed-4a17-9912-7bee82609e87.JPG|PIX133/26a0f945-79cb-4dff-b458-78693f7c565c.JPG"}, "sale_status": "MINIMUM BID", "current_bid": 225, "buy_today_bid": 21500, "sold_price": 0, "sale_date": "2019-05-28T14:00:00Z", "last_update": "2019-05-24T19:12:41Z", "created_at": "2019-05-22T05:40:22.965Z", "updated_at": "2019-05-25T05:37:56.869Z"}, {"bid_status": "NEVER BID", "info": {"lot": 26958689, "vin": "5YJ3E1EB5JF065556", "name": "2018 TESLA MODEL 3 ", "type": "V", "make": "TESLA", "model": "MODEL 3", "year": 2018, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX133/174cf6d3-b668-4152-9d96-267f9620c2c0.JPG", "source": true, "doc_type_ts": "NY", "doc_type_stt": "SM", "doc_type_td": "MV-907A SALVAGE CERTIFICATE", "odometer_orr": 1500, "odometer_ord": "ACTUAL", "lot_highlights": "O", "lot_seller": "", "lot_1st_damage": "STRIPPED", "lot_2nd_damage": "", "retail_value": 63870, "body_style": "", "color": "RED", "engine_type": "", "cylinders": "", "transmission": "", "drive": "All wheel drive", "fuel": "ELECTRIC", "keys": "NO", "notes": "", "location": "NY - SYRACUSE", "lane": "", "item": "", "grid": "", "images": "PIX133/439d6aa3-c145-4250-9ec7-b09bff17222f.JPG|PIX133/3fc74d8d-fccd-4cf0-b9a1-d520c3f72d14.JPG|PIX133/6d08605b-eb60-4ded-889d-e90c0eb8c776.JPG|PIX133/e0954e2b-7695-4050-8f84-79eb7d19017f.JPG|PIX133/93df81c5-8340-48c9-8105-0d2d2e9d1279.JPG|PIX133/13464eed-1247-4fa7-b5e3-0664d6c578a8.JPG|PIX133/0660e5c3-9419-422d-ac24-6f4b2a94e924.JPG|PIX133/7b38d386-1065-4501-b486-0dac84528850.JPG|PIX133/e0b34561-4d82-4af3-8ea8-624fea90f63c.JPG|PIX133/3303d856-e4bb-4fcd-b065-c47e1f879be5.JPG", "thumb_images": "PIX133/174cf6d3-b668-4152-9d96-267f9620c2c0.JPG|PIX133/152dbc5a-5b55-4915-8646-a64d08d0d138.JPG|PIX133/a93b18d9-a6c9-43d1-82db-216730e24140.JPG|PIX133/08708216-c537-4981-94c4-1b740d0244a6.JPG|PIX133/e5800d66-484e-416f-93e4-4ed42a0de9f9.JPG|PIX133/38a5c7ee-613d-41bf-850d-be96167ea8da.JPG|PIX133/67fabcb6-50e0-4cf8-80de-9633a2ac6f7e.JPG|PIX133/70f66e48-dd3d-41f0-b012-236f41da8e84.JPG|PIX133/5b2a2762-8f2a-48eb-b851-03cca67d75f0.JPG|PIX133/8f776141-5d01-4867-9a4e-ce76211c1a4a.JPG"}, "sale_status": "MINIMUM BID", "current_bid": 4600, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-02-26T02:00:00Z", "last_update": "2019-02-20T16:44:45Z", "created_at": "2019-02-20T18:58:48.618Z", "updated_at": "2019-02-20T18:58:48.618Z"}, {"bid_status": "NEVER BID", "info": {"lot": 34731099, "vin": "19UUB1F51JA003507", "name": "2018 ACURA TLX TECH", "type": "V", "make": "ACURA", "model": "TLX TECH", "year": 2018, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX143/7ce4467b-d99b-4068-87df-de9f256b7816.JPG", "source": true, "doc_type_ts": "NJ", "doc_type_stt": "FS", "doc_type_td": "CERT OF TITLE-SALVAGE FLOOD", "odometer_orr": 77, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "WATER/FLOOD", "lot_2nd_damage": "", "retail_value": 36771, "body_style": "", "color": "SILVER", "engine_type": "2.4L  4", "cylinders": "4", "transmission": "", "drive": "Front-wheel Drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "NJ - SOMERVILLE", "lane": "C", "item": "3026", "grid": "*OFF", "images": "PIX143/4fd5dab0-c896-4691-af79-2886377e35f8.JPG|PIX143/e564a585-5b1c-4569-af8e-3440ba492c35.JPG|PIX143/fce48a59-a6ea-439c-9223-3c34d69cc10a.JPG|PIX143/4ea12372-b368-45be-b2d4-3bfadf9f273a.JPG|PIX143/f6b9e7db-dd8f-4dfc-ba44-636d5521488c.JPG|PIX143/fd0351f6-fe68-4ec3-a450-b82552dd3ecf.JPG|PIX143/22c11817-9bcf-45ff-8203-b3dd06a6c3a1.JPG|PIX143/cb05b8ba-eeec-49aa-92ad-ddb40dadf3ae.JPG|PIX143/2a4bd316-ccfa-46c7-93e6-69e09b04f7e2.JPG|PIX143/9f0c1ab6-5213-45f7-89b3-b1e700a80b1c.JPG", "thumb_images": "PIX143/7ce4467b-d99b-4068-87df-de9f256b7816.JPG|PIX143/fa43fcec-29b8-45e7-bd9f-a061e33421c8.JPG|PIX143/61cbc085-7c30-4c64-a645-ee5fa283f72a.JPG|PIX143/a800e6cc-3a0e-4e8f-8387-469dcc9673d7.JPG|PIX143/45267496-b161-434a-bc8e-c473522d1679.JPG|PIX143/28f1cdf4-d31a-42cf-a3b1-636a5bcffd94.JPG|PIX143/dd0508bc-489c-4cf8-a90d-09b45662907f.JPG|PIX143/8053f492-7b09-42b0-ba01-1df3ad0c661f.JPG|PIX143/049c47d0-aefa-4d0d-96ef-04ec8538a53b.JPG|PIX143/68df7cda-fcea-4a05-999b-326b8f44f5c6.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 14500, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-30T01:00:00Z", "last_update": "2019-05-24T15:29:23Z", "created_at": "2019-05-25T06:17:07.705Z", "updated_at": "2019-05-25T06:17:07.705Z"}, {"bid_status": "NEVER BID", "info": {"lot": 31857979, "vin": "2T3JFREVXJW853515", "name": "2018 TOYOTA RAV4 SE", "type": "V", "make": "TOYOTA", "model": "RAV4 SE", "year": 2018, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX133/d20eae13-55c2-43d8-84b2-3909c1057514.JPG", "source": true, "doc_type_ts": "NJ", "doc_type_stt": "FS", "doc_type_td": "CERT OF TITLE-SALVAGE FLOOD", "odometer_orr": 10, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "WATER/FLOOD", "lot_2nd_damage": "", "retail_value": 32847, "body_style": "", "color": "WHITE", "engine_type": "2.5L  4", "cylinders": "4", "transmission": "", "drive": "All wheel drive", "fuel": "GAS", "keys": "YES", "notes": "", "location": "NJ - SOMERVILLE", "lane": "", "item": "0", "grid": "*OFF", "images": "PIX133/c3c6a9c7-34a6-47d3-a45c-b8fb4da8df64.JPG|PIX133/570b87ce-d6ab-4104-b8ed-d01092dfb130.JPG|PIX133/d24a14a2-d163-4f79-b578-d1e15bd0c470.JPG|PIX133/42c0e44a-70ae-4477-9fea-403c063e320b.JPG|PIX133/660e2791-ba39-4a48-a98e-8a9fc2535d74.JPG|PIX133/8ddc8e44-00f5-4db5-8c7e-0b29e62f4f09.JPG|PIX133/bef90dee-9ab8-44f8-b80a-780cd4efb1f6.JPG|PIX133/ebbf4055-c52e-442a-a651-5e43257974a7.JPG|PIX133/812c34b3-967a-43ad-8b1a-9da22b39c5a2.JPG|PIX133/866623e1-23f0-4fc0-9e2c-04dcae310c84.JPG", "thumb_images": "PIX133/d20eae13-55c2-43d8-84b2-3909c1057514.JPG|PIX133/0d2a5abe-8056-4a50-b304-d7887fd7d967.JPG|PIX133/c750c529-107e-42f3-9f1b-3f49ca672306.JPG|PIX133/fc13fb42-2856-4edc-a47f-fa69fc2a1af6.JPG|PIX133/300cd8a6-a198-463d-8f4f-f9bc74853658.JPG|PIX133/1accb367-fdd4-4c6b-8258-9a573a0d5623.JPG|PIX133/db956c4d-eb67-4d18-8b01-0fbae149c0df.JPG|PIX133/c224881e-70b4-4e9d-918f-c4ec7c1a08d6.JPG|PIX133/48950d26-8f14-4744-95a6-2b9f714dee47.JPG|PIX133/96ae0c3b-1d74-40d2-8443-2fe32cae3fb0.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 15700, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-30T01:00:00Z", "last_update": "2019-05-24T15:29:15Z", "created_at": "2019-05-25T05:37:29.677Z", "updated_at": "2019-05-25T05:37:29.677Z"}, {"bid_status": "NEVER BID", "info": {"lot": 33027439, "vin": "1FM5K8D82JGC44980", "name": "2018 FORD EXPLORER XLT", "type": "V", "make": "FORD", "model": "EXPLORER X", "year": 2018, "currency": "USD", "avatar": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/PIX136/7070cf20-a2f2-4278-86d2-4f8e59078fbc.JPG", "source": true, "doc_type_ts": "MA", "doc_type_stt": "CT", "doc_type_td": "CERTIFICATE OF TITLE (P)", "odometer_orr": 11089, "odometer_ord": "ACTUAL", "lot_highlights": "OR", "lot_seller": "", "lot_1st_damage": "SIDE", "lot_2nd_damage": "", "retail_value": 0, "body_style": "", "color": "RED", "engine_type": "3.5L  6", "cylinders": "6", "transmission": "", "drive": "4x4 w/Front Whl Drv", "fuel": "GAS", "keys": "YES", "notes": "", "location": "MA - NORTH BOSTON", "lane": "", "item": "0", "grid": "*OFF", "images": "PIX136/32bf3885-81b1-4504-9898-38955fa0729c.JPG|PIX136/4f8baea7-2704-43ba-84a1-29d49b84838b.JPG|PIX136/49e96c36-b6b3-4811-9fe2-bbbe202ebf6e.JPG|PIX136/a3fdf17b-1b3a-4b84-b706-b82bcdb7fdc4.JPG|PIX136/0913ba25-dd72-4f93-930e-c2be39778214.JPG|PIX136/544f0f9f-25bd-4fb9-9736-36c610ae999f.JPG|PIX136/2b9240ae-7e74-46e3-ab97-daab374a44d8.JPG|PIX136/4670a377-f3d5-4cc7-8e93-200cc0ae46ae.JPG|PIX136/55698038-d03e-4442-8a5c-dd1fc0431ab7.JPG|PIX136/1525ad3c-53f5-4846-89fc-a4b6506a3e6f.JPG", "thumb_images": "PIX136/7070cf20-a2f2-4278-86d2-4f8e59078fbc.JPG|PIX136/b875bdc0-b4e4-41f4-8564-da4c8a18bc94.JPG|PIX136/0cb82783-db26-416d-93ea-10c5a093cd87.JPG|PIX136/6ffdbd79-d1ea-4b0d-88dc-f6b1db6a6ba1.JPG|PIX136/4456cf13-c79c-4d28-9268-cd729d5b7684.JPG|PIX136/a80e2ad7-e4bd-4a20-a1bd-3e3439c2897e.JPG|PIX136/a94ca936-f640-4b1c-95d8-8585915ab5e8.JPG|PIX136/0691de46-df28-4fb9-b12a-c74d86b69820.JPG|PIX136/b44bdc9c-43b0-4727-ab2c-e5fc61b2332f.JPG|PIX136/f9362737-a01b-4bb1-92b4-be616e9d626d.JPG"}, "sale_status": "ON APPROVAL", "current_bid": 19300, "buy_today_bid": 0, "sold_price": 0, "sale_date": "2019-05-30T01:00:00Z", "last_update": "2019-05-24T17:45:54Z", "created_at": "2019-05-25T05:35:34.177Z", "updated_at": "2019-05-25T05:35:34.177Z"}]
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
    } else if (key === 'odometers'){
      let filter = this.applied_filter_odometers.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    } else if (key === 'locations') {
      let filter = this.applied_filter_locations.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    } else if (key === 'sale_dates') {
      let filter = this.applied_filter_sale_dates.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    } else if (key === 'doctypes') {
      let filter = this.applied_filter_doctypes.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    } else if (key === 'vehicle_types') {
      let filter = this.applied_filter_vehicle_types.filter(item => item != value);
      this.changeFilters.emit({"key": key, "value": filter});
    } else if (key === 'damages') {
      let filter = this.applied_filter_damages.filter(item => item != value);
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
    } else if (key === 'cylinderss') {
      let filter = this.applied_filter_cylinders.filter(item => item != value);
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
