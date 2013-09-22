// Generated by LiveScript 1.2.0
(function(){
  'use strict';
  angular.module('roadpinFrontendApp').controller('AppCtrl', ['$scope', '$location', '$resource', '$rootScope', 'version'].concat(function($scope, $location, $resource, $rootScope, version){
    var url;
    url = 'http://106.187.101.193';
    $scope.version = version;
    $scope.$watch('$location.path()', function(activeNavId){
      activeNavId || (activeNavId = '/');
      return $scope.activeNavId = activeNavId, $scope;
    });
    $scope.getClass = function(id){
      if ($scope.activeNavId === id) {
        return 'active';
      } else {
        return '';
      }
    };
    $scope.filterOptions = {
      filterText: "",
      useExternalFilter: true
    };
    $scope.totalServerItems = 0;
    $scope.pagingOptions = {
      pageSizes: [250, 500, 1000],
      pageSize: 250,
      currentPage: 1
    };
    $scope.setPagingData = function(data, page, pageSize){
      var pagedData;
      pagedData = data.slice((page - 1) * pageSize, page * pageSize);
      $scope.myData = pagedData;
      $scope.totalServerItems = data.length;
      if (!$scope.$$phase) {
        return $scope.$apply();
      }
    };
    $scope.getPagedDataAsync = function(pageSize, page, searchText, url){
      return setTimeout(function(){
        var ft;
        if (searchText) {
          ft = searchText.toLowerCase();
          $http.get(url).success(function(largeLoad){
            var data;
            return data = largeLoad.filter(function(item){
              return JSON.stringify(item).toLowerCase().indexOf(ft !== -1);
            });
          });
          return $scope.setPagingData(data, page, pageSize);
        } else {
          $http.get(url).success(function(largeLoad){});
          return $scope.setPagingData(largeLoad, page, pageSize);
        }
      }, 100);
    };
    $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage, url);
    $scope.$watch('pagingOptions', function(newVal, oldVal){
      if (!deepEq$(newVal, oldVal, '===') && !deepEq$(newVal.currentPage, oldVal.currentPage, '===')) {
        return $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage, $scope.filterOptions.filterText, url);
      }
    }, true);
    $scope.$watch('filterOptions', function(newVal, oldVal){
      if (!deepEq$(newVal, oldVal, '===')) {
        return $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage, $scope.filterOptions.filterText, url);
      }
    }, true);
    return $scope.gridOptions = {
      data: 'myData',
      enablePaging: true,
      showFooter: true,
      columnDefs: [
        {
          field: 'county_name',
          displayName: '縣市'
        }, {
          field: 'extension.REG_NAMEpro',
          displayName: '鄉鎮市區'
        }, {
          field: 'extension.CASE_LOCATIONpro',
          displayName: '施工位置'
        }, {
          field: 'extension.CASE_RANGEpro',
          displayName: '施工範圍'
        }, {
          field: 'start_datetime',
          displayName: '開始時間'
        }, {
          field: 'end_datetime',
          displayName: '結束時間'
        }, {
          field: 'extension.CTR_WNAMEpro',
          displayName: '施工單位'
        }, {
          field: 'extension.CTR_ONAMEpro',
          displayName: '監工單位'
        }
      ]
    };
  }));
  function deepEq$(x, y, type){
    var toString = {}.toString, hasOwnProperty = {}.hasOwnProperty,
        has = function (obj, key) { return hasOwnProperty.call(obj, key); };
    var first = true;
    return eq(x, y, []);
    function eq(a, b, stack) {
      var className, length, size, result, alength, blength, r, key, ref, sizeB;
      if (a == null || b == null) { return a === b; }
      if (a.__placeholder__ || b.__placeholder__) { return true; }
      if (a === b) { return a !== 0 || 1 / a == 1 / b; }
      className = toString.call(a);
      if (toString.call(b) != className) { return false; }
      switch (className) {
        case '[object String]': return a == String(b);
        case '[object Number]':
          return a != +a ? b != +b : (a == 0 ? 1 / a == 1 / b : a == +b);
        case '[object Date]':
        case '[object Boolean]':
          return +a == +b;
        case '[object RegExp]':
          return a.source == b.source &&
                 a.global == b.global &&
                 a.multiline == b.multiline &&
                 a.ignoreCase == b.ignoreCase;
      }
      if (typeof a != 'object' || typeof b != 'object') { return false; }
      length = stack.length;
      while (length--) { if (stack[length] == a) { return true; } }
      stack.push(a);
      size = 0;
      result = true;
      if (className == '[object Array]') {
        alength = a.length;
        blength = b.length;
        if (first) { 
          switch (type) {
          case '===': result = alength === blength; break;
          case '<==': result = alength <= blength; break;
          case '<<=': result = alength < blength; break;
          }
          size = alength;
          first = false;
        } else {
          result = alength === blength;
          size = alength;
        }
        if (result) {
          while (size--) {
            if (!(result = size in a == size in b && eq(a[size], b[size], stack))){ break; }
          }
        }
      } else {
        if ('constructor' in a != 'constructor' in b || a.constructor != b.constructor) {
          return false;
        }
        for (key in a) {
          if (has(a, key)) {
            size++;
            if (!(result = has(b, key) && eq(a[key], b[key], stack))) { break; }
          }
        }
        if (result) {
          sizeB = 0;
          for (key in b) {
            if (has(b, key)) { ++sizeB; }
          }
          if (first) {
            if (type === '<<=') {
              result = size < sizeB;
            } else if (type === '<==') {
              result = size <= sizeB
            } else {
              result = size === sizeB;
            }
          } else {
            first = false;
            result = size === sizeB;
          }
        }
      }
      stack.pop();
      return result;
    }
  }
}).call(this);
